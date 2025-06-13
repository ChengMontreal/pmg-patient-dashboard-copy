# # -*- coding: utf-8 -*-

# # Fichier de configuration pour les constantes du projet

# # Nombre de patients synthétiques à générer
# NOMBRE_DE_PATIENTS = 50

# # =============================================================================
# # Le tag <br> est utilisé pour un saut de ligne dans le graphique Plotly
# # =============================================================================

# KPI_COLUMNS = [
#     'Retard Renouvellement (j)<br>(Adhérence thérapeutique)',
#     'Stabilité Financière (%)<br>(Adhérence financière)',
#     'Nb Médicaments Actifs<br>(Condition médicale)',
#     'Polypharmacie (>=5 meds)<br>(Condition médicale)',
#     'Stabilité Assurance (nb plans)<br>(Adhérence financière)'
# ]

# # =============================================================================
# # IMPORTANT : Les clés de ce dictionnaire DOIVENT correspondre exactement
# # aux noms définis dans KPI_COLUMNS ci-dessus.
# # =============================================================================

# KPI_RANGES = {
#     'Retard Renouvellement (j)<br>(Adhérence thérapeutique)': [20, -5],
#     'Stabilité Financière (%)<br>(Adhérence financière)': [70, 100],
#     'Nb Médicaments Actifs<br>(Condition médicale)': [10, 0],
#     'Polypharmacie (>=5 meds)<br>(Condition médicale)': [1, 0],
#     'Stabilité Assurance (nb plans)<br>(Adhérence financière)': [5, 1]
# }
# -*- coding: utf-8 -*-

# Fichier de configuration pour les constantes du projet

# Nombre de patients synthétiques à générer
NOMBRE_DE_PATIENTS = 50

# =============================================================================
# Le tag <br> est utilisé pour un saut de ligne dans le graphique Plotly
# =============================================================================

KPI_COLUMNS = [
    'Score de Ponctualité (%)<br>(Adhérence thérapeutique)',
    'Taux de Succès des Réclamations (%)<br>(Adhérence financière)',
    'Nb Médicaments Actifs<br>(Condition médicale)',
    'Polypharmacie (>=5 meds)<br>(Condition médicale)',
    'Fardeau Financier ($/Rx)<br>(Adhérence financière)'
]

# =============================================================================
# IMPORTANT : Les clés de ce dictionnaire DOIVENT correspondre exactement
# aux noms définis dans KPI_COLUMNS ci-dessus.
# --- CORRECTION: Assurer la cohérence entre les clés et la liste KPI_COLUMNS ---
# =============================================================================

KPI_RANGES = {
    'Score de Ponctualité (%)<br>(Adhérence thérapeutique)': [0, 100],
    'Taux de Succès des Réclamations (%)<br>(Adhérence financière)': [0, 100],
    'Nb Médicaments Actifs<br>(Condition médicale)': [10, 0],
    'Polypharmacie (>=5 meds)<br>(Condition médicale)': [1, 0],
    'Score de Fardeau Financier (%)<br>(Adhérence financière)': [0, 100]
}