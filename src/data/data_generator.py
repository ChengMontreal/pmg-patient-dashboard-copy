# # -*- coding: utf-8 -*-
# import pandas as pd
# import numpy as np
# from datetime import date, timedelta
# from config import NOMBRE_DE_PATIENTS

# def generer_donnees_kroll_synthetiques():
#     """
#     Crée des DataFrames pandas simulant les tables Kroll pertinentes pour tous les KPIs.
#     """
#     patient_ids = [1000 + i for i in range(NOMBRE_DE_PATIENTS)]
    
#     # --- KrollPatient ---
#     patients_df = pd.DataFrame({
#         "id": patient_ids,
#         "LastName": [f"Patient_{i}" for i in range(NOMBRE_DE_PATIENTS)],
#         "FirstName": ["Cheng" if i==0 else "A" for i in range(NOMBRE_DE_PATIENTS)],
#         "Birthday": pd.to_datetime([date(np.random.randint(1950, 2000), np.random.randint(1, 13), np.random.randint(1, 28)) for _ in range(NOMBRE_DE_PATIENTS)])
#     })

#     # --- KrollDrug ---
#     drug_ids = [200 + i for i in range(15)]
#     drugs_df = pd.DataFrame({"id": drug_ids, "BrandName": [f"Médicament_{chr(65+i)}" for i in range(15)]})

#     # --- KrollRxPrescription & KrollRxPrescriptionPlanAdj ---
#     rx_data, rx_adj_data, patient_plan_data = [], [], []
#     rx_num_counter = 5000

#     for pid in patient_ids:
#         # Simuler les plans d'assurance
#         nb_plans = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
#         for i in range(nb_plans):
#             patient_plan_data.append({"PatID": pid, "PlanID": 800+i, "DateCreation": pd.to_datetime(date(2022+i, 1, 1))})

#         # Simuler les prescriptions
#         for i_orig in range(np.random.randint(1, 6)):
#             orig_rx_num = rx_num_counter + pid * 100 + i_orig
#             drug_id = np.random.choice(drug_ids)
#             days_supply = np.random.choice([30, 90])
#             written_date = date(2023, np.random.randint(1, 6), np.random.randint(1, 28))
            
#             nb_fills = np.random.randint(2, 7)
#             last_fill_date = written_date
#             for i_fill in range(nb_fills):
#                 retard = 0 if i_fill == 0 else np.random.randint(-5, 15)
#                 # Ligne corrigée (Corrected Line)
#                 fill_date = last_fill_date + timedelta(days=int(days_supply + retard))
                
#                 rx_data.append({
#                     "RxNum": rx_num_counter, "PatID": pid, "DrgID": drug_id,
#                     "OrigRxNum": orig_rx_num, "FillDate": pd.to_datetime(fill_date),
#                     "DaysSupply": days_supply, "Status": 1
#                 })
                
#                 rx_adj_data.append({
#                     "RxNum": rx_num_counter, "PatID": pid,
#                     "ResultCode": "APPROVED" if np.random.rand() > 0.15 else "REJECTED"
#                 })

#                 last_fill_date = fill_date
#                 rx_num_counter += 1

#     rx_df = pd.DataFrame(rx_data)
#     rx_adj_df = pd.DataFrame(rx_adj_data)
#     patient_plan_df = pd.DataFrame(patient_plan_data)
    
#     return patients_df, drugs_df, rx_df, rx_adj_df, patient_plan_df

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import date, timedelta
from config import NOMBRE_DE_PATIENTS

def generer_donnees_kroll_synthetiques():
    """
    Crée des DataFrames pandas simulant les tables Kroll pertinentes pour tous les KPIs.
    """
    patient_ids = [1000 + i for i in range(NOMBRE_DE_PATIENTS)]
    
    # --- KrollPatient ---
    patients_df = pd.DataFrame({
        "id": patient_ids,
        "LastName": [f"Patient_{i}" for i in range(NOMBRE_DE_PATIENTS)],
        "FirstName": ["Cheng" if i==0 else "A" for i in range(NOMBRE_DE_PATIENTS)],
        "Birthday": pd.to_datetime([date(np.random.randint(1950, 2000), np.random.randint(1, 13), np.random.randint(1, 28)) for _ in range(NOMBRE_DE_PATIENTS)])
    })

    # --- KrollDrug ---
    drug_ids = [200 + i for i in range(15)]
    drugs_df = pd.DataFrame({"id": drug_ids, "BrandName": [f"Médicament_{chr(65+i)}" for i in range(15)]})

    # --- KrollRxPrescription & KrollRxPrescriptionPlanAdj ---
    rx_data, rx_adj_data, patient_plan_data = [], [], []
    rx_num_counter = 5000

    for pid in patient_ids:
        # Simuler les plans d'assurance
        nb_plans = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
        for i in range(nb_plans):
            patient_plan_data.append({"PatID": pid, "PlanID": 800+i, "DateCreation": pd.to_datetime(date(2022+i, 1, 1))})

        # Simuler les prescriptions
        for i_orig in range(np.random.randint(1, 6)):
            orig_rx_num = rx_num_counter + pid * 100 + i_orig
            drug_id = np.random.choice(drug_ids)
            days_supply = np.random.choice([30, 90])
            written_date = date(2023, np.random.randint(1, 6), np.random.randint(1, 28))
            
            nb_fills = np.random.randint(2, 7)
            last_fill_date = written_date
            for i_fill in range(nb_fills):
                retard = 0 if i_fill == 0 else np.random.randint(-5, 15)
                
                # --- CORRECTION: Convertir les types numpy en int standard ---
                fill_date = last_fill_date + timedelta(days=int(days_supply) + int(retard))
                
                rx_data.append({
                    "RxNum": rx_num_counter, "PatID": pid, "DrgID": drug_id,
                    "OrigRxNum": orig_rx_num, "FillDate": pd.to_datetime(fill_date),
                    "DaysSupply": int(days_supply), # S'assurer que le type est cohérent
                    "Status": 1
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
    
    return patients_df, drugs_df, rx_df, rx_adj_df, patient_plan_df