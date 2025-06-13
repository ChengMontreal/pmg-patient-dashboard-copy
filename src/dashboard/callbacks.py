# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
from src.dashboard.plots import creer_glyph_plot
from config import KPI_COLUMNS

def register_callbacks(app, df_kpis, profils_groupes):
    """
    Enregistre toutes les callbacks de l'application.
    """
    @app.callback(
        [Output('patient-info', 'children'),
         Output('kpi-patient-graph', 'figure'),
         Output('kpi-groupe-graph', 'figure')],
        [Input('patient-dropdown', 'value')]
    )
    def update_dashboard(selected_patient_id):
        if not selected_patient_id:
            return dash.no_update

        patient_data = df_kpis[df_kpis['patient_id'] == selected_patient_id].iloc[0]
        groupe = patient_data['groupe_age']
        groupe_data = profils_groupes[profils_groupes['groupe_age'] == groupe].iloc[0]
        
        patient_kpis = patient_data[KPI_COLUMNS]
        groupe_kpis = groupe_data[KPI_COLUMNS]

        fig_patient = creer_glyph_plot(patient_kpis, f"Profil Individuel: {patient_data['FirstName']}", KPI_COLUMNS)
        fig_groupe = creer_glyph_plot(groupe_kpis, f"Profil Moyen du Groupe: {groupe}", KPI_COLUMNS)

        info_text = f"Patient: {patient_data['FirstName']} {patient_data['LastName']} | Âge: {patient_data['age']} | Groupe: {groupe}"
        
        return info_text, fig_patient, fig_groupe