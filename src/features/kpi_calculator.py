# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from functools import reduce # 引入reduce来优雅地合并多个dataframe
from config import KPI_COLUMNS

def calculer_score_ponctualite(jours):
    """
    Calcule un score de ponctualité de 0 à 100 basé sur le retard en jours.
    Une fenêtre "idéale" est définie pour le score maximum.
    """
    # Fenêtre idéale: de 7 jours en avance (-7) à 3 jours de retard (+3)
    if -7 <= jours <= 3:
        return 100
    # Pénalité pour le retard (plus sévère)
    elif jours > 3:
        # Chaque jour de retard après la fenêtre de grâce coûte 4 points
        return max(0, 100 - (jours - 3) * 4)
    # Pénalité pour le renouvellement trop précoce (moins sévère)
    else: # jours < -7
        # Chaque jour trop en avance coûte 2 points
        return max(0, 100 - (abs(jours) - 7) * 2)

def calculer_kpis(patients, drugs, rx, rx_adj, patient_plans):
    """
    Calcule tous les KPIs pour chaque patient, avec tous les KPIs normalisés sur une échelle de 0-100.
    """
    # ... (KPI 1, 2, 3, 4 calculations remain the same) ...
    # --- KPI 1: Score de Ponctualité des Renouvellements ---
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
    if not rx_adj.empty:
        adj_summary = rx_adj.groupby('PatID')['ResultCode'].apply(lambda x: (x == 'APPROVED').sum() / len(x) * 100 if len(x) > 0 else 0).round(0).reset_index()
        adj_summary.rename(columns={'ResultCode': KPI_COLUMNS[1]}, inplace=True)
    else:
        adj_summary = pd.DataFrame(columns=['PatID', KPI_COLUMNS[1]])

    # --- KPI 3: Complexité Médicale ---
    un_an_avant = pd.Timestamp.now() - pd.DateOffset(years=1)
    kpi_complexite = rx[rx['FillDate'] > un_an_avant].groupby('PatID')['DrgID'].nunique().reset_index()
    kpi_complexite.rename(columns={'DrgID': KPI_COLUMNS[2]}, inplace=True)

    # --- KPI 4: Polypharmacie ---
    trois_mois_avant = pd.Timestamp.now() - pd.DateOffset(months=3)
    meds_recents = rx[rx['FillDate'] > trois_mois_avant]
    kpi_polypharm_count = meds_recents.groupby('PatID')['DrgID'].nunique().reset_index(name='RecentDrugCount')
    kpi_polypharm_count[KPI_COLUMNS[3]] = (kpi_polypharm_count['RecentDrugCount'] >= 5).astype(int)
    
    # --- KPI 5: Score de Fardeau Financier (%) (NOUVELLE LOGIQUE DE NORMALISATION) ---
    kpi_fardeau_financier = pd.DataFrame() # Initialiser un dataframe vide
    if not rx_adj.empty and not rx.empty:
        if 'Cost' not in rx.columns:
            rx['Cost'] = np.random.uniform(20, 150, size=len(rx))
            rx['Fee'] = 10
        rx_costs = rx[['RxNum', 'Cost', 'Fee']]
        rx_adj_costs = pd.merge(rx_adj, rx_costs, on='RxNum', how='left')
        rx_adj_costs['CoutTotal'] = rx_adj_costs['Cost'] + rx_adj_costs['Fee']
        if 'PlanPays' not in rx_adj_costs.columns:
            rx_adj_costs['PlanPays'] = rx_adj_costs.apply(lambda row: row['CoutTotal'] * np.random.uniform(0.7, 1.0) if row['ResultCode'] == 'APPROVED' else 0, axis=1)
        rx_adj_costs['PartPatient'] = (rx_adj_costs['CoutTotal'] - rx_adj_costs['PlanPays']).clip(lower=0)
        
        # Calculer le fardeau moyen en dollars
        df_burden_dollars = rx_adj_costs.groupby('PatID')['PartPatient'].mean().round(2).reset_index()
        
        # --- Transformation en score 0-100 ---
        PIRE_FARDEAU = 50  # 50$ ou plus = score 0 (pire cas)
        MEILLEUR_FARDEAU = 0 # 0$ = score 100 (meilleur cas)
        
        df_burden_dollars['Score'] = 100 * (PIRE_FARDEAU - df_burden_dollars['PartPatient']) / (PIRE_FARDEAU - MEILLEUR_FARDEAU)
        df_burden_dollars['Score'] = df_burden_dollars['Score'].clip(0, 100).astype(int)
        
        kpi_fardeau_financier = df_burden_dollars[['PatID', 'Score']].copy()
        kpi_fardeau_financier.rename(columns={'Score': KPI_COLUMNS[4]}, inplace=True)
    
    if kpi_fardeau_financier.empty:
         kpi_fardeau_financier = pd.DataFrame(columns=['PatID', KPI_COLUMNS[4]])
    
    # ... (La logique de fusion reste la même) ...
    kpi_dfs = [
        kpi_adherence_ther,
        adj_summary,
        kpi_complexite,
        kpi_polypharm_count,
        kpi_fardeau_financier
    ]
    df_merged_kpis = reduce(lambda left, right: pd.merge(left, right, on='PatID', how='outer'), kpi_dfs)
    if 'RecentDrugCount' in df_merged_kpis.columns:
        df_merged_kpis.drop(columns=['RecentDrugCount'], inplace=True)
    df = pd.merge(patients, df_merged_kpis, left_on='id', right_on='PatID', how='left')
    if 'PatID' in df.columns:
        df.drop(columns=['PatID'], inplace=True)
    df['age'] = ((pd.Timestamp.now() - df['Birthday']).dt.days / 365.25).astype(int)
    for col in KPI_COLUMNS:
        if col in df.columns:
            if col in [KPI_COLUMNS[2], KPI_COLUMNS[3]]:
                 df[col] = df[col].fillna(0)
    final_kpi_cols = [col for col in KPI_COLUMNS if col in df.columns]
    final_cols = ['id', 'LastName', 'FirstName', 'age'] + final_kpi_cols
    final_df = df[final_cols].copy()
    final_df.rename(columns={'id': 'patient_id'}, inplace=True)
    
    return final_df

def segmenter_patients(df_kpis):
    """
    Segmente les patients par groupe d'âge et calcule le profil moyen du groupe.
    """
    bins = [0, 40, 60, 120] 
    labels = ["<40 ans", "40-60 ans", ">60 ans"]
    df_kpis['groupe_age'] = pd.cut(df_kpis['age'], bins=bins, labels=labels, right=False)
    
    # Créer une copie pour éviter le SettingWithCopyWarning
    df_kpis_copy = df_kpis.copy()
    
    profils_groupes = df_kpis_copy.groupby('groupe_age', observed=False)[KPI_COLUMNS].mean(numeric_only=True).round(2).reset_index()
    
    return df_kpis_copy, profils_groupes

