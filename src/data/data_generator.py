# Fichier: src/data/data_generator.py
# Description: Génère des données synthétiques plus réalistes en utilisant des distributions statistiques.
import pandas as pd
import numpy as np
from datetime import date, timedelta
from config import NOMBRE_DE_PATIENTS

def generer_donnees_kroll_synthetiques():
    """
    Crée des DataFrames pandas simulant les tables Kroll pertinentes.
    Utilise des distributions statistiques pour un meilleur réalisme.
    """
    patient_ids = [1000 + i for i in range(NOMBRE_DE_PATIENTS)]
    
    # --- KrollPatient ---
    patients_df = pd.DataFrame({
        "id": patient_ids,
        "LastName": [f"Patient_{i}" for i in range(NOMBRE_DE_PATIENTS)],
        "FirstName": ["Cheng" if i==0 else "A" for i in range(NOMBRE_DE_PATIENTS)],
        "Birthday": pd.to_datetime([date(np.random.randint(1950, 2000), np.random.randint(1, 13), np.random.randint(1, 28)) for _ in range(NOMBRE_DE_PATIENTS)])
    })

    # --- Pathologies et Médicaments ---
    pathologies = ['Diabète', 'Hypertension', 'Asthme', 'Dépression']
    categories_meds = ['Antidiabétique', 'Antihypertenseur', 'Bronchodilatateur', 'Antidépresseur', 'Analgésique']
    
    # --- KrollDrug (avec catégories et coûts réalistes) ---
    drug_ids = [200 + i for i in range(20)]
    drugs_df = pd.DataFrame({
        "id": drug_ids, 
        "BrandName": [f"Médicament_{chr(65+i)}" for i in range(20)],
        # Coûts suivant une distribution log-normale
        "Cost": np.round(np.random.lognormal(mean=3.5, sigma=0.7, size=20), 2),
        "Fee": 10.0,
        "Categorie": [np.random.choice(categories_meds) for _ in range(20)]
    })

    # --- KrollPatientCnd (nouvelle table pour les pathologies) ---
    patient_cnd_data = []
    for pid in patient_ids:
        # Chaque patient a 1 ou 2 pathologies
        for _ in range(np.random.randint(1, 3)):
             patient_cnd_data.append({"PatID": pid, "Code": np.random.choice(pathologies)})
    patient_cnd_df = pd.DataFrame(patient_cnd_data)


    # --- KrollRxPrescription & KrollRxPrescriptionPlanAdj ---
    rx_data, rx_adj_data, patient_plan_data = [], [], []
    rx_num_counter = 5000

    for pid in patient_ids:
        # Simuler les plans d'assurance
        nb_plans = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
        for i in range(nb_plans):
            patient_plan_data.append({"PatID": pid, "PlanID": 800+i})

        # Simuler les prescriptions (nombre de prescriptions par patient suit une loi de Poisson)
        nb_prescriptions = np.random.poisson(lam=4) + 1 # Au moins 1 prescription
        for _ in range(nb_prescriptions):
            orig_rx_num = rx_num_counter + pid * 100 + _
            drug_id = np.random.choice(drug_ids)
            days_supply = np.random.choice([30, 90])
            written_date = date(2023, np.random.randint(1, 6), np.random.randint(1, 28))
            
            nb_fills = np.random.poisson(lam=3) + 2 # Au moins 2 remplissages
            last_fill_date = written_date
            
            for i_fill in range(nb_fills):
                # Le retard suit une distribution Gamma pour simuler une "longue traîne"
                # shape=2, scale=3 -> la plupart des retards sont faibles, quelques-uns sont élevés
                # On soustrait 7 pour centrer la distribution autour de -1 (renouvellement un peu en avance)
                retard = int(np.round(np.random.gamma(shape=2, scale=3) - 7))
                
                fill_date = last_fill_date + timedelta(days=int(days_supply) + retard)
                
                rx_data.append({
                    "RxNum": rx_num_counter, "PatID": pid, "DrgID": drug_id,
                    "OrigRxNum": orig_rx_num, "FillDate": pd.to_datetime(fill_date),
                    "DaysSupply": int(days_supply),
                })
                
                rx_adj_data.append({
                    "RxNum": rx_num_counter, "PatID": pid,
                    "ResultCode": "APPROVED" if np.random.rand() > 0.15 else "REJECTED"
                })

                last_fill_date = fill_date
                rx_num_counter += 1

    rx_df = pd.DataFrame(rx_data)
    rx_adj_df = pd.DataFrame(rx_adj_data)
    patient_plan_df = pd.DataFrame(patient_plan_data)
    
    # Retourner toutes les tables, y compris la nouvelle table des pathologies
    return patients_df, drugs_df, rx_df, rx_adj_df, patient_plan_df, patient_cnd_df