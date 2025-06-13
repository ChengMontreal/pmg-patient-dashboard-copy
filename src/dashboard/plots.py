# -*- coding: utf-8 -*-
import plotly.graph_objects as go
from config import KPI_RANGES
import pandas as pd


def creer_glyph_plot(kpi_data, titre, kpi_names):
    """
    Crée une figure Scatterpolar (Glyph Plot) normalisée.
    Un score plus élevé (plus éloigné du centre) est toujours meilleur.
    """
    normalized_values = []
    for col in kpi_names:
        # S'assurer que la colonne existe avant de tenter d'y accéder
        if col not in kpi_data or pd.isna(kpi_data[col]):
            normalized_values.append(0) # Mettre une valeur par défaut (0) si le KPI est manquant
            continue
            
        val = kpi_data[col]
        
        # Si la colonne n'est pas dans KPI_RANGES, cela signifie qu'elle est déjà sur une échelle de 0-100
        if col not in KPI_RANGES:
            score = val
        else:
            pire, meilleur = KPI_RANGES[col]
            
            # La logique de normalisation pour les KPIs où plus bas est meilleur (ex: Nb Médicaments)
            if meilleur < pire:
                score = 100 * (pire - val) / (pire - meilleur) if (pire - meilleur) != 0 else 0
            # La logique pour les KPIs où plus haut est meilleur (déjà un score 0-100)
            else:
                score = 100 * (val - pire) / (meilleur - pire) if (meilleur - pire) != 0 else 0
        
        normalized_values.append(max(0, min(100, score)))

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=kpi_names,
        fill='toself',
        name='Profil Normalisé'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title=titre,
        title_x=0.5,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig