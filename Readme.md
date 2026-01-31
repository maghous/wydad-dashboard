# 🔴⚪ Wydad Athletic Club - Application d'Analyse Statistique

## 📋 Description

Application web professionnelle développée avec Streamlit pour analyser les performances du **Wydad Athletic Club** de 2011 à 2025. Cette application offre une visualisation interactive et complète des statistiques des joueurs, performances d'équipe, et analyses avancées.

## ✨ Fonctionnalités Principales

### 🏠 Tableau de Bord Général
- KPIs principaux (Joueurs, Buts, Passes, Valeur totale)
- Répartition des joueurs par position
- Distribution des âges
- Évolution des performances par saison

### 📈 Analyses de Performances
- **Attaque**: Top buteurs, contributions offensives
- **Défense**: Statistiques de discipline, cartons
- **Temps de Jeu**: Répartition des minutes, joueurs les plus utilisés

### 👥 Profils des Joueurs
- Recherche individuelle de joueurs
- Statistiques détaillées par saison
- Comparaison entre deux joueurs (Radar Chart)
- Évolution des performances

### 💰 Valeur Marchande
- Analyse de la valeur totale et moyenne
- Top 10 joueurs les plus chers
- Valeur par position
- Évolution de la valeur par saison

### 📊 Analyses Avancées
- **Efficacité**: Ratios buts/match, minutes/but
- **Corrélations**: Matrice de corrélation entre variables
- **Records**: Hall of Fame, statistiques remarquables

## 🚀 Installation et Utilisation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner ou télécharger les fichiers**
```bash
# Si vous avez les fichiers localement
cd chemin/vers/le/dossier
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
streamlit run wydad_app.py
```

4. **Accéder à l'application**
- L'application s'ouvrira automatiquement dans votre navigateur
- Sinon, accédez à: `http://localhost:8501`

## 📊 Utilisation des Données Réelles

Pour utiliser vos propres données du Wydad:

1. **Préparez votre fichier CSV** avec les colonnes suivantes:
   - Name (nom du joueur)
   - Position
   - Age
   - Matchs
   - Buts
   - Passes décisives
   - Minutes jouées
   - Cartons Jaunes
   - CartonS rouges
   - market_value (valeur marchande)
   - Saison (format: 2011/12)
   - PPM (points par match)
   - Taille (optionnel)
   - Pied (optionnel)

2. **Modifiez la fonction `load_data()`** dans `wydad_app.py`:
```python
@st.cache_data
def load_data():
    # Remplacez par le chemin vers votre fichier
    df = pd.read_csv('wydad.csv')
    
    # Ajouter les colonnes calculées
    df['Ratio_Buts_Matchs'] = df['Buts'] / df['Matchs'].replace(0, np.nan)
    df['Minutes_par_match'] = df['Minutes jouées'] / df['Matchs'].replace(0, np.nan)
    df['Contributions_offensives'] = df['Buts'] + df['Passes décisives']
    df['Cartons_total'] = df['Cartons Jaunes'] + df['CartonS rouges']
    
    return df
```

## 🎨 Personnalisation

### Couleurs
Les couleurs du Wydad (Rouge et Blanc) sont définies dans le CSS:
- Rouge principal: `#DC143C`
- Rouge foncé: `#B22222`
- Rouge très foncé: `#8B0000`

Pour modifier les couleurs, éditez la section `st.markdown()` au début du fichier.

### Logo
Pour ajouter le logo officiel du Wydad:
1. Placez le fichier image dans le même dossier
2. Modifiez la ligne dans la sidebar:
```python
st.image("chemin/vers/logo.png", width=150)
```

## 📱 Fonctionnalités Interactives

- **Filtres**: Sélectionnez des saisons et positions spécifiques
- **Navigation**: 5 pages thématiques accessibles depuis la sidebar
- **Graphiques interactifs**: Zoom, survol pour détails, exportation
- **Responsive**: Fonctionne sur desktop, tablette et mobile

## 🔧 Technologies Utilisées

- **Streamlit**: Framework web pour applications de data science
- **Pandas**: Manipulation et analyse de données
- **Plotly**: Visualisations interactives
- **NumPy**: Calculs numériques

## 📈 Structure du Projet

```
wydad_app/
│
├── wydad_app.py          # Application principale
├── requirements.txt      # Dépendances Python
├── README.md            # Documentation
└── wydad.csv            # Données (à ajouter)
```

## 🎯 Cas d'Usage

- **Analyse de recrutement**: Identifier les meilleurs joueurs par position
- **Suivi des performances**: Évolution des joueurs saison par saison
- **Analyse financière**: Optimisation de la valeur de l'effectif
- **Comparaison**: Benchmarking entre joueurs
- **Reporting**: Génération de rapports visuels pour la direction

## 🤝 Support et Contribution

Pour toute question ou suggestion d'amélioration:
- Créez une issue sur le dépôt
- Proposez des pull requests
- Contactez l'équipe de développement

## 📜 Licence

Ce projet est développé pour honorer le Wydad Athletic Club et ses supporters.

## 🏆 À Propos du Wydad

Le **Wydad Athletic Club** (WAC), fondé en 1937 à Casablanca, est l'un des clubs les plus titrés d'Afrique avec de nombreux championnats nationaux et continentaux à son palmarès.

**DiMa Wydad!** 🔴⚪

---

Créé avec ❤️ pour les Winners