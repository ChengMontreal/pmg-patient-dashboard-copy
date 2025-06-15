# Fichier: app.py
import dash
import pandas as pd
from sqlalchemy import create_engine
from src.features.kpi_calculator import calculer_kpis, segmenter_patients
from src.dashboard.layout import create_layout
from src.dashboard.callbacks import register_callbacks

DB_FILE = "kroll_demo.db"
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE}"

def charger_donnees_depuis_db(engine):
    print("Chargement des données depuis la base de données...")
    try:
        patients = pd.read_sql_table('kroll_patient', engine, parse_dates=['Birthday'])
        drugs = pd.read_sql_table('kroll_drug', engine)
        rx = pd.read_sql_table('kroll_rx_prescription', engine, parse_dates=['FillDate'])
        rx_adj = pd.read_sql_table('kroll_rx_prescription_plan_adj', engine)
        patient_plans = pd.read_sql_table('kroll_patient_plan', engine)
        # Charger la nouvelle table
        patient_cnd = pd.read_sql_table('kroll_patient_cnd', engine)
        print("Données chargées avec succès.")
        return patients, drugs, rx, rx_adj, patient_plans, patient_cnd
    except Exception as e:
        print(f"ERREUR: Impossible de charger les données depuis '{DB_FILE}'.")
        print(f"Veuillez vous assurer d'avoir exécuté 'python creer_base_de_donnees.py' d'abord.")
        print(f"Détail de l'erreur: {e}")
        exit()

db_engine = create_engine(DB_CONNECTION_STRING)

# Passer la nouvelle table aux fonctions suivantes
patients, drugs, rx, rx_adj, patient_plans, patient_cnd = charger_donnees_depuis_db(db_engine)

print("Calcul des KPIs...")
df_kpis = calculer_kpis(patients, drugs, rx, rx_adj, patient_plans, patient_cnd)
df_kpis_final, profils_groupes = segmenter_patients(df_kpis, rx, drugs, patient_cnd)
print("Préparation du tableau de bord terminée.")

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.title = "PMG Patient Dashboard"

app.layout = create_layout(df_kpis_final)
# Passer tous les dataframes nécessaires aux callbacks
register_callbacks(app, df_kpis_final, profils_groupes)
if __name__ == '__main__':
    app.run_server(debug=True)