# Fichier: config.py

# Nombre de patients synthétiques à générer
NOMBRE_DE_PATIENTS = 1000

# Le tag <br> est utilisé pour un saut de ligne dans le graphique Plotly
KPI_COLUMNS = [
    'Score de Ponctualité (%)<br>(Adhérence thérapeutique)',
    'Taux de Succès des Réclamations (%)<br>(Adhérence financière)',
    'Nb Médicaments Actifs<br>(Condition médicale)',
    'Polypharmacie (>=5 meds)<br>(Condition médicale)',
    # CORRECTION: Nom du KPI harmonisé pour correspondre à KPI_RANGES
    'Score de Fardeau Financier (%)<br>(Adhérence financière)'
]

# IMPORTANT : Les clés de ce dictionnaire DOIVENT correspondre exactement
# aux noms définis dans KPI_COLUMNS ci-dessus.
KPI_RANGES = {
    'Score de Ponctualité (%)<br>(Adhérence thérapeutique)': [0, 100],
    'Taux de Succès des Réclamations (%)<br>(Adhérence financière)': [0, 100],
    'Nb Médicaments Actifs<br>(Condition médicale)': [10, 0],
    'Polypharmacie (>=5 meds)<br>(Condition médicale)': [1, 0],
    'Score de Fardeau Financier (%)<br>(Adhérence financière)': [0, 100]
}