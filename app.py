import dash
import pandas as pd
from sqlalchemy import create_engine
from src.features.kpi_calculator import calculer_kpis, segmenter_patients
from src.dashboard.layout import create_layout
from src.dashboard.callbacks import register_callbacks

# --- CONFIGURATION ---
DB_FILE = "kroll_demo.db"
DB_CONNECTION_STRING = f"sqlite:///{DB_FILE}"

def charger_donnees_depuis_db(engine):
    """
    Charge toutes les tables nécessaires depuis la base de données dans des DataFrames pandas.
    """
    print("Chargement des données depuis la base de données...")
    try:
        patients = pd.read_sql_table('kroll_patient', engine)
        drugs = pd.read_sql_table('kroll_drug', engine)
        rx = pd.read_sql_table('kroll_rx_prescription', engine, parse_dates=['FillDate', 'Birthday'])
        rx_adj = pd.read_sql_table('kroll_rx_prescription_plan_adj', engine)
        patient_plans = pd.read_sql_table('kroll_patient_plan', engine)
        print("Données chargées avec succès.")
        return patients, drugs, rx, rx_adj, patient_plans
    except Exception as e:
        print(f"ERREUR: Impossible de charger les données depuis '{DB_FILE}'.")
        print(f"Veuillez vous assurer d'avoir exécuté 'python creer_base_de_donnees.py' d'abord.")
        print(f"Détail de l'erreur: {e}")
        # Quitter si la base de données n'est pas accessible
        exit()

# 1. Préparation des données
# Crée le moteur de connexion à la base de données
db_engine = create_engine(DB_CONNECTION_STRING)

# Charge les données depuis la base de données au lieu de les générer à la volée
patients, drugs, rx, rx_adj, patient_plans = charger_donnees_depuis_db(db_engine)

print("Calcul des KPIs...")
df_kpis = calculer_kpis(patients, drugs, rx, rx_adj, patient_plans)
df_kpis_final, profils_groupes = segmenter_patients(df_kpis)
print("Préparation du tableau de bord terminée.")

# 2. Initialisation de l'application Dash
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server
app.title = "PMG Patient Dashboard"

# 3. Définition de la mise en page et des callbacks
app.layout = create_layout(df_kpis_final)
register_callbacks(app, df_kpis_final, profils_groupes)

# 4. Lancement du serveur
if __name__ == '__main__':
    app.run_server(debug=True)
