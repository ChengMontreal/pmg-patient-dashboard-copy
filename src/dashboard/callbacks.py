# # -*- coding: utf-8 -*-
# from dash.dependencies import Input, Output
# from src.dashboard.plots import creer_glyph_plot
# from config import KPI_COLUMNS

# def register_callbacks(app, df_kpis, profils_groupes):
#     """
#     Enregistre toutes les callbacks de l'application.
#     """
#     @app.callback(
#         [Output('patient-info', 'children'),
#          Output('kpi-patient-graph', 'figure'),
#          Output('kpi-groupe-graph', 'figure')],
#         [Input('patient-dropdown', 'value')]
#     )
#     def update_dashboard(selected_patient_id):
#         if not selected_patient_id:
#             return dash.no_update

#         patient_data = df_kpis[df_kpis['patient_id'] == selected_patient_id].iloc[0]
#         groupe = patient_data['groupe_age']
#         groupe_data = profils_groupes[profils_groupes['groupe_age'] == groupe].iloc[0]
        
#         patient_kpis = patient_data[KPI_COLUMNS]
#         groupe_kpis = groupe_data[KPI_COLUMNS]

#         fig_patient = creer_glyph_plot(patient_kpis, f"Profil Individuel: {patient_data['FirstName']}", KPI_COLUMNS)
#         fig_groupe = creer_glyph_plot(groupe_kpis, f"Profil Moyen du Groupe: {groupe}", KPI_COLUMNS)

#         info_text = f"Patient: {patient_data['FirstName']} {patient_data['LastName']} | Âge: {patient_data['age']} | Groupe: {groupe}"
        
#         return info_text, fig_patient, fig_groupe

# Fichier: src/dashboard/callbacks.py
from dash.dependencies import Input, Output, State
import dash
from src.dashboard.plots import creer_glyph_plot_compare, creer_scatter_plot_correlation
from config import KPI_COLUMNS

def register_callbacks(app, df_kpis, profils_groupes):
    """
    Enregistre toutes les callbacks de l'application.
    """
    # Callback pour le graphique de comparaison (radar)
    @app.callback(
        [Output('patient-info', 'children'),
         Output('kpi-comparison-graph', 'figure')],
        [Input('patient-dropdown', 'value'),
         Input('segment-type-dropdown', 'value')]
    )
    def update_comparison_dashboard(selected_patient_id, segment_type):
        if not selected_patient_id:
            return dash.no_update

        patient_data = df_kpis[df_kpis['patient_id'] == selected_patient_id].iloc[0]
        
        # Logique pour trouver le bon groupe et profil
        groupe_df = profils_groupes[segment_type]
        colonne_segment = ''
        valeur_segment = ''
        
        if segment_type == 'Âge':
            colonne_segment = 'groupe_age'
            valeur_segment = patient_data['groupe_age']
        elif segment_type == 'Pathologie':
            colonne_segment = 'pathologie'
            valeur_segment = patient_data['pathologie']
        elif segment_type == 'Médicament':
            colonne_segment = 'med_categorie'
            valeur_segment = patient_data['med_categorie']
            
        groupe_data = groupe_df[groupe_df[colonne_segment] == valeur_segment]
        
        # Gérer le cas où un patient n'a pas de groupe (ex: pas de patho)
        if groupe_data.empty:
            # On peut prendre la moyenne de tous les patients comme fallback
            groupe_data = df_kpis[KPI_COLUMNS].mean(numeric_only=True)
            titre_groupe = "Moyenne Globale"
        else:
            groupe_data = groupe_data.iloc[0]
            titre_groupe = f"Groupe {valeur_segment}"

        fig_comparison = creer_glyph_plot_compare(
            patient_data[KPI_COLUMNS], 
            groupe_data, 
            f"Profil Comparatif: {patient_data['FirstName']} vs. {titre_groupe}", 
            KPI_COLUMNS
        )

        info_text = f"Patient: {patient_data['FirstName']} {patient_data['LastName']} | Âge: {patient_data['age']} | Pathologie: {patient_data['pathologie']}"
        
        return info_text, fig_comparison

    # Nouveau callback pour le graphique de corrélation (scatter)
    @app.callback(
        Output('correlation-scatter-plot', 'figure'),
        [Input('xaxis-kpi', 'value'),
         Input('yaxis-kpi', 'value')]
    )
    def update_scatter_plot(kpi_x, kpi_y):
        if not kpi_x or not kpi_y:
            return dash.no_update
        
        fig = creer_scatter_plot_correlation(df_kpis, kpi_x, kpi_y)
        return fig