# Fichier: src/features/kpi_calculator.py
import pandas as pd
import numpy as np
from functools import reduce
from config import KPI_COLUMNS

def calculer_score_ponctualite(jours):
    if -7 <= jours <= 3: return 100
    elif jours > 3: return max(0, 100 - (jours - 3) * 4)
    else: return max(0, 100 - (abs(jours) - 7) * 2)

def calculer_kpis(patients, drugs, rx, rx_adj, patient_plans, patient_cnd):
    """
    Calcule tous les KPIs pour chaque patient.
    """
    rx_avec_cout = pd.merge(rx, drugs[['id', 'Cost', 'Fee']], left_on='DrgID', right_on='id', how='left').drop(columns=['id'])
    
    # --- KPI 1: Score de Ponctualité ---
    rx_sorted = rx.sort_values(by=['PatID', 'OrigRxNum', 'FillDate'])
    rx_sorted['PrevFillDate'] = rx_sorted.groupby(['PatID', 'OrigRxNum'])['FillDate'].shift(1)
    rx_sorted['PrevDaysSupply'] = rx_sorted.groupby(['PatID', 'OrigRxNum'])['DaysSupply'].shift(1)
    rx_sorted.dropna(subset=['PrevFillDate'], inplace=True)
    rx_sorted['DateRenouvellementAttendue'] = rx_sorted['PrevFillDate'] + pd.to_timedelta(rx_sorted['PrevDaysSupply'], unit='d')
    rx_sorted['RetardJours'] = (rx_sorted['FillDate'] - rx_sorted['DateRenouvellementAttendue']).dt.days
    rx_sorted['ScorePonctualite'] = rx_sorted['RetardJours'].apply(calculer_score_ponctualite)
    kpi_adherence_ther = rx_sorted.groupby('PatID')['ScorePonctualite'].mean().round(0).astype(int).reset_index()
    kpi_adherence_ther.rename(columns={'ScorePonctualite': KPI_COLUMNS[0]}, inplace=True)

    # --- KPI 2: Taux de Succès des Réclamations ---
    adj_summary = rx_adj.groupby('PatID')['ResultCode'].apply(lambda x: (x == 'APPROVED').sum() / len(x) * 100 if len(x) > 0 else 0).round(0).reset_index()
    adj_summary.rename(columns={'ResultCode': KPI_COLUMNS[1]}, inplace=True)

    # --- KPI 3 & 4: Complexité Médicale & Polypharmacie ---
    un_an_avant = pd.Timestamp.now() - pd.DateOffset(years=1)
    kpi_complexite = rx[rx['FillDate'] > un_an_avant].groupby('PatID')['DrgID'].nunique().reset_index()
    kpi_complexite.rename(columns={'DrgID': KPI_COLUMNS[2]}, inplace=True)
    
    trois_mois_avant = pd.Timestamp.now() - pd.DateOffset(months=3)
    meds_recents = rx[rx['FillDate'] > trois_mois_avant]
    kpi_polypharm_count = meds_recents.groupby('PatID')['DrgID'].nunique().reset_index(name='RecentDrugCount')
    kpi_polypharm_count[KPI_COLUMNS[3]] = (kpi_polypharm_count['RecentDrugCount'] >= 5).astype(int)
    
    # --- KPI 5: Score de Fardeau Financier ---
    rx_adj_costs = pd.merge(rx_adj, rx_avec_cout[['RxNum', 'Cost', 'Fee']], on='RxNum', how='left')
    rx_adj_costs.fillna(0, inplace=True)
    rx_adj_costs['CoutTotal'] = rx_adj_costs['Cost'] + rx_adj_costs['Fee']
    rx_adj_costs['PlanPays'] = rx_adj_costs.apply(lambda row: row['CoutTotal'] * np.random.uniform(0.7, 1.0) if row['ResultCode'] == 'APPROVED' else 0, axis=1)
    rx_adj_costs['PartPatient'] = (rx_adj_costs['CoutTotal'] - rx_adj_costs['PlanPays']).clip(lower=0)
    
    df_burden_dollars = rx_adj_costs.groupby('PatID')['PartPatient'].mean().round(2).reset_index()
    PIRE_FARDEAU, MEILLEUR_FARDEAU = 50, 0
    df_burden_dollars['Score'] = 100 * (PIRE_FARDEAU - df_burden_dollars['PartPatient']) / (PIRE_FARDEAU - MEILLEUR_FARDEAU)
    kpi_fardeau_financier = df_burden_dollars[['PatID', 'Score']].copy()
    kpi_fardeau_financier.rename(columns={'Score': KPI_COLUMNS[4]}, inplace=True)
    kpi_fardeau_financier[KPI_COLUMNS[4]] = kpi_fardeau_financier[KPI_COLUMNS[4]].clip(0, 100).astype(int)

    # --- Fusion et finalisation ---
    df_merged = patients.copy()
    kpi_dfs_to_merge = [kpi_adherence_ther, adj_summary, kpi_complexite, kpi_polypharm_count[['PatID', KPI_COLUMNS[3]]], kpi_fardeau_financier]
    
    for kpi_df in kpi_dfs_to_merge:
        df_merged = pd.merge(df_merged, kpi_df, left_on='id', right_on='PatID', how='left')
        if 'PatID' in df_merged.columns:
            df_merged.drop(columns='PatID', inplace=True)
            
    df_merged['age'] = ((pd.Timestamp.now() - df_merged['Birthday']).dt.days / 365.25).astype(int)
    final_kpi_cols = [col for col in KPI_COLUMNS if col in df_merged.columns]
    final_cols = ['id', 'LastName', 'FirstName', 'age'] + final_kpi_cols
    final_df = df_merged[final_cols].copy()
    final_df.rename(columns={'id': 'patient_id'}, inplace=True)
    
    for col in final_kpi_cols:
        final_df[col] = final_df[col].fillna(0)

    return final_df

def segmenter_patients(df_kpis, rx, drugs, patient_cnd):
    """
    Segmente les patients selon plusieurs dimensions (âge, pathologie, catégorie de médicament)
    et retourne un dictionnaire de profils moyens.
    """
    profils_groupes = {}
    df_kpis_copy = df_kpis.copy()

    # --- 1. Segmentation par Âge ---
    bins = [0, 40, 60, 120] 
    labels = ["<40 ans", "40-60 ans", ">60 ans"]
    df_kpis_copy['groupe_age'] = pd.cut(df_kpis_copy['age'], bins=bins, labels=labels, right=False)
    profils_groupes['Âge'] = df_kpis_copy.groupby('groupe_age', observed=False)[KPI_COLUMNS].mean(numeric_only=True).round(2).reset_index()

    # --- 2. Segmentation par Pathologie ---
    patient_main_patho = patient_cnd.groupby('PatID')['Code'].agg(lambda x: x.value_counts().index[0]).reset_index()
    patient_main_patho.rename(columns={'Code': 'pathologie'}, inplace=True)
    df_kpis_with_patho = pd.merge(df_kpis_copy, patient_main_patho, left_on='patient_id', right_on='PatID', how='left')
    profils_groupes['Pathologie'] = df_kpis_with_patho.groupby('pathologie')[KPI_COLUMNS].mean(numeric_only=True).round(2).reset_index()

    # --- 3. Segmentation par Catégorie de Médicament ---
    rx_with_cat = pd.merge(rx, drugs[['id', 'Categorie']], left_on='DrgID', right_on='id', how='left')
    patient_main_cat = rx_with_cat.groupby('PatID')['Categorie'].agg(lambda x: x.value_counts().index[0]).reset_index()
    patient_main_cat.rename(columns={'Categorie': 'med_categorie'}, inplace=True)
    df_kpis_with_cat = pd.merge(df_kpis_copy, patient_main_cat, left_on='patient_id', right_on='PatID', how='left')
    profils_groupes['Médicament'] = df_kpis_with_cat.groupby('med_categorie')[KPI_COLUMNS].mean(numeric_only=True).round(2).reset_index()
    
    # --- Ajout des colonnes de segmentation au dataframe principal ---
    final_df = pd.merge(df_kpis_copy, patient_main_patho[['PatID', 'pathologie']], left_on='patient_id', right_on='PatID', how='left')
    final_df = pd.merge(final_df, patient_main_cat[['PatID', 'med_categorie']], left_on='patient_id', right_on='PatID', how='left')
    # Supprimer les colonnes PatID redondantes après les fusions
    final_df.drop(columns=['PatID_x', 'PatID_y'], inplace=True, errors='ignore')

    # CORRECTION: Remplacer les NaN uniquement dans les colonnes pertinentes AVANT de retourner le dataframe
    final_df['pathologie'] = final_df['pathologie'].fillna('N/A')
    final_df['med_categorie'] = final_df['med_categorie'].fillna('N/A')
    
    return final_df, profils_groupes