# Fichier: creer_base_de_donnees.py
# Description: Script pour générer des données synthétiques et peupler une base de données SQLite.
#              À n'exécuter qu'une seule fois pour initialiser la base de données.
import pandas as pd
from src.data.data_generator import generer_donnees_kroll_synthetiques
from src.data.KrollDatabase import Base 
from sqlalchemy import create_engine

DB_FILE = "kroll_demo.db"
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE}"

def initialiser_base_de_donnees():
    print(f"Création de la connexion à la base de données '{DB_FILE}'...")
    engine = create_engine(DB_CONNECTION_STRING)

    print("Création des tables du schéma Kroll...")
    Base.metadata.create_all(engine)
    print("Tables créées avec succès.")

    print("Génération des données synthétiques en mémoire...")
    # Récupérer le nouveau dataframe patient_cnd_df
    patients_df, drugs_df, rx_df, rx_adj_df, patient_plans_df, patient_cnd_df = generer_donnees_kroll_synthetiques()
    print("Données générées.")

    print("Écriture des données dans la base de données...")
    
    patients_df.to_sql('kroll_patient', engine, if_exists='replace', index=False)
    print("- Table 'kroll_patient' peuplée.")
    
    drugs_df.to_sql('kroll_drug', engine, if_exists='replace', index=False)
    print("- Table 'kroll_drug' peuplée.")
    
    patient_plans_df.to_sql('kroll_patient_plan', engine, if_exists='replace', index=False)
    print("- Table 'kroll_patient_plan' peuplée.")
    
    rx_df.to_sql('kroll_rx_prescription', engine, if_exists='replace', index=False)
    print("- Table 'kroll_rx_prescription' peuplée.")
    
    rx_adj_df.to_sql('kroll_rx_prescription_plan_adj', engine, if_exists='replace', index=False)
    print("- Table 'kroll_rx_prescription_plan_adj' peuplée.")

    # Ajouter la nouvelle table à la base de données
    patient_cnd_df.to_sql('kroll_patient_cnd', engine, if_exists='replace', index=False)
    print("- Table 'kroll_patient_cnd' peuplée.")
    
    print("\nLa base de données a été initialisée avec succès!")

if __name__ == '__main__':
    initialiser_base_de_donnees()