
# Description: Script pour générer des données synthétiques et peupler une base de données SQLite.
#              À n'exécuter qu'une seule fois pour initialiser la base de données.
import pandas as pd
from sqlalchemy import create_engine
from src.data.data_generator import generer_donnees_kroll_synthetiques
from src.data.KrollDatabase import Base  # Importer la Base depuis le fichier corrigé

# --- CONFIGURATION ---
DB_FILE = "kroll_demo.db"
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE}"

def initialiser_base_de_donnees():
    """
    Crée les tables et charge les données synthétiques dans la base de données SQLite.
    """
    # Étape 1: Créer une connexion à la base de données
    print(f"Création de la connexion à la base de données '{DB_FILE}'...")
    engine = create_engine(DB_CONNECTION_STRING)

    # Étape 2: Créer toutes les tables définies dans KrollDatabase.py
    print("Création des tables du schéma Kroll...")
    Base.metadata.create_all(engine)
    print("Tables créées avec succès.")

    # Étape 3: Générer les données synthétiques en utilisant la fonction existante
    print("Génération des données synthétiques en mémoire...")
    patients_df, drugs_df, rx_df, rx_adj_df, patient_plans_df = generer_donnees_kroll_synthetiques()
    print("Données générées.")

    # Étape 4: Écrire les DataFrames dans la base de données
    print("Écriture des données dans la base de données. Cette opération peut prendre un moment...")
    
    # Utiliser la méthode to_sql de pandas pour un chargement simple et efficace.
    # 'if_exists='replace'' supprimera les données existantes avant de charger les nouvelles.
    # 'index=False' évite d'écrire l'index du DataFrame comme une colonne SQL.
    
    patients_df.to_sql('kroll_patient', engine, if_exists='replace', index=False)
    print("- Table 'kroll_patient' peuplée.")
    
    drugs_df.to_sql('kroll_drug', engine, if_exists='replace', index=False)
    print("- Table 'kroll_drug' peuplée.")
    
    # Assurer que les noms de colonnes du DataFrame correspondent à la table de destination
    patient_plans_df.to_sql('kroll_patient_plan', engine, if_exists='replace', index=False)
    print("- Table 'kroll_patient_plan' peuplée.")
    
    rx_df.to_sql('kroll_rx_prescription', engine, if_exists='replace', index=False)
    print("- Table 'kroll_rx_prescription' peuplée.")
    
    # Pour rx_adj_df, il se peut que le nom de la table soit 'kroll_rx_prescription_plan_adj'
    # Il faut s'assurer que le DataFrame contient les colonnes nécessaires (ex: RxNum, PatID, ResultCode)
    rx_adj_df.to_sql('kroll_rx_prescription_plan_adj', engine, if_exists='replace', index=False)
    print("- Table 'kroll_rx_prescription_plan_adj' peuplée.")
    
    print("\nLa base de données a été initialisée avec succès!")
    print(f"Le fichier '{DB_FILE}' est prêt à être utilisé par l'application.")

if __name__ == '__main__':
    initialiser_base_de_donnees()