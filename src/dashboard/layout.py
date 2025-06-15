# # -*- coding: utf-8 -*-
# from dash import dcc, html

# def create_layout(df_kpis):
#     """
#     Crée la mise en page (layout) de l'application Dash.
#     """
#     return html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
#         html.H1("Tableau de Bord - Profil Patient", style={'textAlign': 'center', 'color': '#003366'}),
#         html.P("Analyse personnalisée des profils patients comparés à des populations de référence.", style={'textAlign': 'center'}),
        
#         html.Div([
#             html.Label("Sélectionner un patient:"),
#             dcc.Dropdown(
#                 id='patient-dropdown',
#                 options=[{'label': f"{row['FirstName']} {row['LastName']} ({row['patient_id']})", 'value': row['patient_id']} 
#                          for index, row in df_kpis.iterrows()],
#                 value=df_kpis['patient_id'].iloc[0]
#             )
#         ], style={'width': '50%', 'margin': '20px auto'}),
        
#         html.Div(id='patient-info', style={'textAlign': 'center', 'fontSize': '1.2em', 'marginBottom': '20px'}),

#         html.Div(className='row', children=[
#             html.Div(dcc.Graph(id='kpi-patient-graph'), className='six columns', style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
#             html.Div(dcc.Graph(id='kpi-groupe-graph'), className='six columns', style={'width': '49%', 'display': 'inline-block', 'float': 'right', 'verticalAlign': 'top'})
#         ])
#     ])

# Fichier: src/dashboard/layout.py
from dash import dcc, html
from config import KPI_COLUMNS

def create_layout(df_kpis):
    """
    Crée la mise en page (layout) de l'application Dash avec les nouveaux contrôles.
    """
    return html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
        html.H1("Tableau de Bord - Profil Patient", style={'textAlign': 'center', 'color': '#003366'}),
        
        # --- Section de sélection du patient et du groupe ---
        html.Div(className='row', style={'marginBottom': '20px'}, children=[
            # Sélection du patient
            html.Div(className='six columns', children=[
                html.Label("1. Sélectionner un patient:"),
                dcc.Dropdown(
                    id='patient-dropdown',
                    options=[{'label': f"{row['FirstName']} {row['LastName']} ({row['patient_id']})", 'value': row['patient_id']} 
                             for index, row in df_kpis.iterrows()],
                    value=df_kpis['patient_id'].iloc[0]
                )
            ]),
            # Sélection du type de groupe
            html.Div(className='six columns', children=[
                html.Label("2. Comparer avec le groupe par:"),
                dcc.Dropdown(
                    id='segment-type-dropdown',
                    options=[
                        {'label': 'Âge', 'value': 'Âge'},
                        {'label': 'Pathologie', 'value': 'Pathologie'},
                        {'label': 'Catégorie de Médicament', 'value': 'Médicament'}
                    ],
                    value='Âge'
                )
            ])
        ]),

        html.Div(id='patient-info', style={'textAlign': 'center', 'fontSize': '1.2em', 'marginBottom': '20px'}),
        
        # Graphique de comparaison (radar chart)
        html.Div(dcc.Graph(id='kpi-comparison-graph'), style={'width': '60%', 'margin': '0 auto'}),

        html.Hr(style={'margin': '40px 0'}),

        # --- Section d'analyse de la population ---
        html.H2("Analyse de la Population", style={'textAlign': 'center', 'color': '#003366'}),
        html.P("Explorez les corrélations entre les différents KPIs sur l'ensemble des patients.", style={'textAlign': 'center'}),

        html.Div(className='row', style={'marginTop': '20px'}, children=[
            # Sélection de l'axe X
            html.Div(className='six columns', children=[
                html.Label("Axe X:"),
                dcc.Dropdown(id='xaxis-kpi', options=[{'label': k.replace('<br>', ' '), 'value': k} for k in KPI_COLUMNS], value=KPI_COLUMNS[0])
            ]),
            # Sélection de l'axe Y
            html.Div(className='six columns', children=[
                html.Label("Axe Y:"),
                dcc.Dropdown(id='yaxis-kpi', options=[{'label': k.replace('<br>', ' '), 'value': k} for k in KPI_COLUMNS], value=KPI_COLUMNS[1])
            ])
        ]),
        
        # Graphique de corrélation (scatter plot)
        html.Div(dcc.Graph(id='correlation-scatter-plot'))
    ])