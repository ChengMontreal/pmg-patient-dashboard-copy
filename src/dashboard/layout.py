# -*- coding: utf-8 -*-
from dash import dcc, html

def create_layout(df_kpis):
    """
    Crée la mise en page (layout) de l'application Dash.
    """
    return html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
        html.H1("Tableau de Bord - Profil Patient", style={'textAlign': 'center', 'color': '#003366'}),
        html.P("Analyse personnalisée des profils patients comparés à des populations de référence.", style={'textAlign': 'center'}),
        
        html.Div([
            html.Label("Sélectionner un patient:"),
            dcc.Dropdown(
                id='patient-dropdown',
                options=[{'label': f"{row['FirstName']} {row['LastName']} ({row['patient_id']})", 'value': row['patient_id']} 
                         for index, row in df_kpis.iterrows()],
                value=df_kpis['patient_id'].iloc[0]
            )
        ], style={'width': '50%', 'margin': '20px auto'}),
        
        html.Div(id='patient-info', style={'textAlign': 'center', 'fontSize': '1.2em', 'marginBottom': '20px'}),

        html.Div(className='row', children=[
            html.Div(dcc.Graph(id='kpi-patient-graph'), className='six columns', style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div(dcc.Graph(id='kpi-groupe-graph'), className='six columns', style={'width': '49%', 'display': 'inline-block', 'float': 'right', 'verticalAlign': 'top'})
        ])
    ])