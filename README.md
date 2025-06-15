# Tableau de Bord d'Analyse Patient

Une application web interactive développée avec Plotly Dash pour visualiser le profil de santé d'un patient.

Le projet analyse des données de pharmacie simulées pour calculer une série d'indicateurs de performance clés (KPIs), permettant de comparer un individu à des groupes de référence (par âge, pathologie, etc.).

## Aperçu Visuel

![Aperçu du Dashboard](https://i.imgur.com/7xXq070.png)

## Fonctionnalités Clés

* **Profil Comparatif (Graphique Radar)**: Compare les KPIs d'un patient à la moyenne de son groupe de référence. Tous les scores sont normalisés sur une échelle de 0 à 100, où un score plus élevé est toujours meilleur.
* **Analyse de Corrélation (Nuage de Points)**: Permet d'explorer visuellement la relation entre deux indicateurs sur l'ensemble de la population de patients.
* **Filtres Interactifs**: Sélectionnez dynamiquement un patient et le segment de population (âge, pathologie, etc.) pour une analyse sur mesure.

---

## Logique des Indicateurs (KPIs)

Le modèle calcule 5 KPIs pour évaluer le profil d'un patient sous différents angles.

#### 1. Score de Ponctualité (%) `(Adhérence thérapeutique)`

Cet indicateur mesure à quel point un patient respecte le calendrier de renouvellement de ses médicaments.
* **Logique de calcul**:
    1.  Pour chaque prescription, on identifie la date du renouvellement précédent et la durée d'approvisionnement (`DaysSupply`).
    2.  On calcule la "date de renouvellement attendue" (`date précédent + DaysSupply`).
    3.  On mesure l'écart en jours entre la date réelle et la date attendue.
    4.  Un score est attribué via une fonction qui tolère une fenêtre de temps idéale (ex: 7 jours avant à 3 jours après la date prévue), et pénalise progressivement les écarts plus importants.

#### 2. Taux de Succès des Réclamations (%) `(Adhérence financière)`

Reflète la capacité du patient à gérer ses soumissions d'assurance sans problème.
* **Logique de calcul**: C'est le ratio simple des réclamations approuvées par rapport au nombre total de réclamations soumises : `(nb_approuvées / nb_total) * 100`.

#### 3. Nb Médicaments Actifs & Polypharmacie `(Condition médicale)`

Ces deux indicateurs évaluent la complexité médicale du patient.
* **Logique de calcul**:
    * **Nb Médicaments Actifs**: On compte le nombre de médicaments uniques (`nunique`) servis au patient au cours de la dernière année.
    * **Polypharmacie**: On vérifie si ce nombre de médicaments actifs est supérieur ou égal à 5, un seuil de risque clinique reconnu. C'est un indicateur binaire (1 pour Oui, 0 pour Non).
* *Pour le score du graphique radar, une valeur brute plus faible (moins de médicaments) donne un score normalisé plus élevé.*

#### 4. Score de Fardeau Financier (%) `(Adhérence financière)`

Évalue l'impact des coûts des médicaments sur le patient.
* **Logique de calcul**:
    1.  Pour chaque prescription, on calcule la part payée par le patient (`coût_total - part_payée_par_l_assurance`).
    2.  On calcule la moyenne de ces coûts pour le patient.
    3.  Cette moyenne est ensuite transformée en un score sur 100. Plus le coût moyen pour le patient est bas, plus le score final est élevé.

---

## Stack Technique

* [cite_start]**Analyse de Données**: Pandas, NumPy 
* [cite_start]**Tableau de Bord**: Plotly, Dash 
* [cite_start]**Base de Données**: SQLAlchemy (avec un backend SQLite) 

---

## Installation et Lancement

#### 1. Prérequis

* Python (version 3.9+ recommandée)
* `git` pour cloner le dépôt

#### 2. Instructions

1.  **Cloner le dépôt**
    ```bash
    git clone <url-du-repo>
    cd <nom-du-repo>
    ```

2.  **Créer un environnement virtuel et installer les dépendances**
    ```bash
    # Créer et activer un environnement virtuel (recommandé)
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate

    # Installer les librairies requises
    pip install -r requirements.txt
    ```

3.  **Initialiser la base de données**
    Ce script génère les données simulées. Il ne doit être exécuté **qu'une seule fois**.
    ```bash
    python creer_base_de_donnees.py
    ```

4.  **Lancer l'application**
    ```bash
    python app.py
    ```
    Le tableau de bord sera ensuite accessible à l'adresse `http://127.0.0.1:8050/`.

---

## Évolutions et Intégration

Ce projet constitue un prototype entièrement fonctionnel. Pour une intégration dans un environnement de production plus large (avec des technologies comme **Angular** ou **Node.js**), l'architecture pourrait évoluer :

* **API Backend**: La logique de calcul des KPIs (`kpi_calculator.py`) pourrait être exposée via une **API REST**. Cette API recevrait un ID de patient et retournerait ses données de profil au format JSON.
* **Frontend**: Une application développée en **Angular** (ou une autre technologie web) pourrait alors consommer les données de cette API pour afficher le graphique radar au sein d'une interface utilisateur plus vaste et complexe.

## Notes Techiniques
Le modèle de calcul des KPIs pour ce projet a été implémenté avec succès. Pour accélérer la phase de validation, des données synthétiques ont été générées. Celles-ci incluent des champs de convenance (Cost, Fee et Categorie) qui ont été ajoutés à la table des médicaments (KrollDrug) mais qui ne font pas partie du schéma officiel.

Pour une connexion à une base de données Kroll de production qui respecte strictement le schéma, l'étape de pré-traitement des données nécessiterait les ajustements suivants :

Les coûts des médicaments (Cost, Fee) pour les indicateurs financiers devraient être extraits de la table KrollRxPrescription.
La classification des médicaments (Categorie) devrait probablement utiliser le champ ProductType existant ou être mappée selon les règles métier de l'entreprise.