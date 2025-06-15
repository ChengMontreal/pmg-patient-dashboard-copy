# Fichier: src/dashboard/plots.py
# Description: Contient toutes les fonctions de création de graphiques pour le tableau de bord.

import plotly.graph_objects as go
import pandas as pd
from config import KPI_RANGES

def normaliser_kpi(kpi_data, kpi_names):
    """
    Fonction helper pour normaliser une série de KPIs en scores de 0-100.
    Un score plus élevé est toujours meilleur.
    """
    normalized_values = []
    for col in kpi_names:
        # Gérer le cas où le KPI est manquant pour un patient/groupe
        if col not in kpi_data or pd.isna(kpi_data[col]):
            normalized_values.append(0) 
            continue
            
        val = kpi_data[col]
        
        # Si la colonne n'est pas dans KPI_RANGES, c'est déjà un score de 0-100
        if col not in KPI_RANGES:
            score = val
        else:
            pire, meilleur = KPI_RANGES[col]
            
            # Normalisation pour les KPIs où une valeur plus basse est meilleure
            if meilleur < pire:
                score = 100 * (pire - val) / (pire - meilleur) if (pire - meilleur) != 0 else 0
            # Normalisation pour les KPIs où une valeur plus élevée est meilleure
            else:
                score = 100 * (val - pire) / (meilleur - pire) if (meilleur - pire) != 0 else 0
        
        # S'assurer que le score reste dans l'intervalle [0, 100]
        normalized_values.append(max(0, min(100, score)))
    return normalized_values

def creer_glyph_plot_compare(patient_kpis, groupe_kpis, titre, kpi_names):
    """
    Crée une figure Scatterpolar qui superpose les données du patient et du groupe.
    C'est la fonction qui manquait.
    """
    # Normaliser les deux séries de données
    patient_scores = normaliser_kpi(patient_kpis, kpi_names)
    groupe_scores = normaliser_kpi(groupe_kpis, kpi_names)

    fig = go.Figure()

    # Trace pour le groupe (en fond, semi-transparent)
    fig.add_trace(go.Scatterpolar(
        r=groupe_scores,
        theta=kpi_names,
        fill='toself',
        name='Moyenne du Groupe',
        fillcolor='rgba(0, 100, 255, 0.2)',
        line=dict(color='rgba(0, 100, 255, 0.4)')
    ))

    # Trace pour le patient (au premier plan, ligne solide)
    fig.add_trace(go.Scatterpolar(
        r=patient_scores,
        theta=kpi_names,
        fill='toself',
        name='Profil du Patient',
        fillcolor='rgba(255, 100, 0, 0.2)',
        line=dict(color='rgba(255, 100, 0, 1)')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title=titre,
        title_x=0.5,
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

def creer_scatter_plot_correlation(df, kpi_x, kpi_y):
    """
    Crée un scatter plot pour explorer la corrélation entre deux KPIs.
    """
    # Calculer le coefficient de corrélation pour l'afficher dans le titre
    correlation = df[kpi_x].corr(df[kpi_y]).round(2)
    
    fig = go.Figure(data=go.Scatter(
        x=df[kpi_x],
        y=df[kpi_y],
        mode='markers',
        marker=dict(
            size=8,
            color=df['age'], 
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Âge")
        ),
        text=df.apply(lambda row: f"{row['FirstName']} {row['LastName']}", axis=1),
        hovertemplate='<b>%{text}</b><br>' +
                      '%{xaxis.title.text}: %{x}<br>' +
                      '%{yaxis.title.text}: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title=f"Corrélation entre les KPIs (r = {correlation})",
        xaxis_title=kpi_x.replace('<br>', ' '),
        yaxis_title=kpi_y.replace('<br>', ' '),
        title_x=0.5,
        plot_bgcolor='rgba(240,240,240,0.95)'
    )
    return fig