# Tableau de Bord des Indicateurs Clés de Performance (KPI) Patient

Ce projet est une solution de démonstration conçue pour répondre à un mandat d'analyse de données patient. L'objectif est de modéliser une série de KPIs (Indicateurs Clés de Performance) cliniques et comportementaux pour permettre une analyse personnalisée du profil d'un patient, tout en le comparant à des populations de référence.

La solution simule un environnement réel en utilisant une base de données **SQLite** pour stocker les données transactionnelles, qui sont ensuite lues par un tableau de bord interactif construit avec **Python**, **Pandas**, **SQLAlchemy** et **Plotly Dash**.

## Aperçu du Tableau de Bord
![Aperçu](https://i.imgur.com/7xXq070.png)
*(Note: L'image est un exemple représentatif de l'interface.)*

## Objectifs du Projet

- **Créer un langage commun** entre les données transactionnelles, les soins cliniques et les décisions.
- **Démontrer la valeur des données administratives** pour rendre les soins plus humains et adaptés.
- **Ouvrir la voie** à des applications futures comme la stratification des risques et la recommandation clinique.

## Indicateurs Clés de Performance (KPIs) Implémentés

Le tableau de bord analyse les KPIs suivants, qui sont normalisés en scores où une valeur plus élevée indique une meilleure performance :

1.  **Score de Ponctualité (%)**: Mesure l'adhérence thérapeutique en évaluant la ponctualité des renouvellements de prescriptions. Un score de 100% est accordé pour un renouvellement dans une fenêtre de temps idéale.
2.  **Taux de Succès des Réclamations (%)**: Reflète l'adhérence financière en calculant le pourcentage de soumissions aux assurances qui sont approuvées sans problème.
3.  **Nb Médicaments Actifs**: Indique la complexité médicale par le nombre de médicaments uniques qu'un patient a pris au cours de la dernière année.
4.  **Polypharmacie (>=5 meds)**: Un indicateur binaire (1 pour Oui, 0 pour Non) signalant si un patient prend 5 médicaments ou plus simultanément, un facteur de risque clinique important.
5.  **Score de Fardeau Financier (%)**: Évalue l'impact financier sur le patient en transformant le coût moyen par prescription payé par le patient en un score. Un score élevé signifie un fardeau financier faible.

## Stack Technique

-   **Backend & Analyse de Données**: Python 3.11, Pandas, NumPy
-   **Base de Données**: SQLite
-   **ORM (Mappage Objet-Relationnel)**: SQLAlchemy
-   **Tableau de Bord Interactif**: Plotly Dash
-   **Gestion de l'Environnement**: Conda

## Structure du Projet