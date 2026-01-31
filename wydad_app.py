import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Configuration de la page
st.set_page_config(
    page_title="Wydad Athletic Club - Analyse Statistique",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé Premium (Wydad Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Poppins:wght@300;400;600&display=swap');
    
    /* Global */
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Titres */
    h1, h2, h3, .title-wydad {
        font-family: 'Oswald', sans-serif !important;
        color: #1A1A1A;
        text-transform: uppercase;
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(135deg, #E61717 0%, #B22222 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 6px rgba(230, 23, 23, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(230, 23, 23, 0.4);
    }
    
    /* KPI Cards */
    .stat-box {
        background: white;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border-bottom: 4px solid #E61717;
        transition: transform 0.3s ease;
    }
    .stat-box:hover {
        transform: translateY(-5px);
    }
    .stat-number {
        font-family: 'Oswald', sans-serif;
        font-size: 2.8em;
        font-weight: 700;
        color: #E61717;
        margin-bottom: 5px;
    }
    .stat-label {
        color: #666;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #eee;
    }
    
    /* Header Principal */
    .header-container {
        text-align: center;
        padding: 40px 0;
        background: radial-gradient(circle at center, #fff 0%, #f8f9fa 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 4em;
        color: #E61717;
        text-shadow: 2px 2px 0px #000;
        margin: 0;
        line-height: 1.2;
    }
    .sub-title {
        font-size: 1.5em;
        color: #D4AF37; /* Gold */
        font-weight: bold;
        letter-spacing: 2px;
        font-family: 'Oswald', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data
def load_data():
    """Charge et prépare les données du Wydad"""
    try:
        # Chemin de base (relatif pour compatibilité Cloud & Local)
        base_path = 'data'
        
        # Liste des fichiers à charger
        files = [
            'Merged_WYDAD_201112.csv',
            'Merged_WYDAD_201213.csv',
            'Merged_WYDAD_201314.csv',
            'Merged_WYDAD_201415.csv',
            'Merged_WYDAD_201516.csv',
            'Merged_WYDAD_201617.csv',
            'Merged_WYDAD_201718.csv',
            'Merged_WYDAD_201819.csv',
            'Merged_WYDAD_201920.csv',
            'Merged_WYDAD_202021.csv',
            'Merged_WYDAD_202122.csv',
            'Merged_WYDAD_202223.csv',
            'Merged_WYDAD_202324.csv',
            'Merged_WYDAD_202425.csv'
        ]
        
        # Charger tous les fichiers
        dfs = []
        for file in files:
            file_path = os.path.join(base_path, file)
            try:
                df_temp = pd.read_csv(file_path, encoding='utf-8')
                dfs.append(df_temp)
                # st.sidebar.success(f"✅ {file} chargé")
            except FileNotFoundError:
                st.sidebar.warning(f"⚠️ Fichier non trouvé: {file}")
            except Exception as e:
                st.sidebar.error(f"❌ Erreur avec {file}: {str(e)}")
        
        if dfs:
            df = pd.concat(dfs, ignore_index=True)
            # st.sidebar.success(f"✅ Total: {len(df)} enregistrements chargés")
        else:
            raise FileNotFoundError("Aucun fichier trouvé")
            
    except Exception as e:
        st.error(f"⚠️ Erreur: {str(e)}")
        st.info("📊 Utilisation de données d'exemple pour la démonstration")
        
        # Données d'exemple
        data = {
            'Name': ['Nadir Lamyaghri', 'Mourad Lemsen', 'Youssef Rabeh', 'Hicham Amrani', 
                     'Ayoub El Kaabi', 'Yahya Jabrane', 'Walid El Karti'] * 15,
            'Position': ['Gardien de but', 'Défense', 'Défenseur central', 'Défenseur central',
                        'Avant-centre', 'Milieu central', 'Ailier droit'] * 15,
            'Age': [34, 31, 26, 25, 28, 27, 24] * 15,
            'Matchs': [21, 25, 23, 24, 30, 28, 20] * 15,
            'Buts': [0, 1, 0, 1, 15, 5, 8] * 15,
            'Passes décisives': [0, 2, 0, 1, 3, 8, 6] * 15,
            'Minutes jouées': [1890, 2245, 2070, 2147, 2700, 2520, 1800] * 15,
            'Cartons Jaunes': [0, 6, 2, 8, 3, 4, 2] * 15,
            'CartonS rouges': [0, 0, 0, 0, 0, 1, 0] * 15,
            'market_value': [275000, 150000, 200000, 180000, 800000, 600000, 450000] * 15,
            'Saison': ['2011/12', '2012/13', '2013/14', '2014/15', '2015/16', 
                      '2016/17', '2017/18', '2018/19', '2019/20', '2020/21',
                      '2021/22', '2022/23', '2023/24', '2024/25', '2011/12'] * 7,
            'PPM': [1.90, 1.68, 1.65, 1.58, 2.10, 1.95, 1.75] * 15
        }
        df = pd.DataFrame(data)
    
    # Nettoyer et convertir les colonnes numériques
    numeric_cols = ['Age', 'Matchs', 'Buts', 'Passes décisives', 'Minutes jouées', 
                    'Cartons Jaunes', 'CartonS rouges', 'market_value', 'PPM']
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remplacer les NaN par 0 pour certaines colonnes
    df['Buts'] = df['Buts'].fillna(0)
    df['Passes décisives'] = df['Passes décisives'].fillna(0)
    df['Cartons Jaunes'] = df['Cartons Jaunes'].fillna(0)
    df['CartonS rouges'] = df['CartonS rouges'].fillna(0)
    df['market_value'] = df['market_value'].fillna(0)
    
    # Ajouter des colonnes calculées
    df['Ratio_Buts_Matchs'] = df['Buts'] / df['Matchs'].replace(0, np.nan)
    df['Minutes_par_match'] = df['Minutes jouées'] / df['Matchs'].replace(0, np.nan)
    df['Contributions_offensives'] = df['Buts'] + df['Passes décisives']
    df['Cartons_total'] = df['Cartons Jaunes'] + df['CartonS rouges']
    
    return df

# Chargement des données
df = load_data()

# En-tête de l'application
col_logo, col_title = st.columns([1, 4])

with col_title:
    st.markdown("""
        <div class="header-container">
            <h1 class="main-title">WYDAD ATHLETIC CLUB</h1>
            <p class="sub-title">DASHBOARD ANALYTIQUE • DEPUIS 1937</p>
        </div>
    """, unsafe_allow_html=True)

with col_logo:
    st.image("wydad_logo.png", width=180)

st.markdown("---")

# Sidebar pour la navigation
with st.sidebar:
    st.markdown("## 🔴 WYDAD AC")
    st.markdown("## 📊 Navigation")
    
    page = st.radio(
        "Sélectionner une page",
        ["🏠 Tableau de Bord", 
         "📈 Performances", 
         "👥 Joueurs", 
         "💰 Valeur Marchande",
         "📊 Analyses Avancées"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Filtres")
    
    # Filtre par saison
    saisons = ['Toutes'] + sorted(df['Saison'].unique().tolist())
    saison_selectionnee = st.selectbox("Saison", saisons)
    
    # Filtre par position
    positions = ['Toutes'] + sorted(df['Position'].unique().tolist())
    position_selectionnee = st.selectbox("Position", positions)
    
    # Appliquer les filtres
    df_filtered = df.copy()
    if saison_selectionnee != 'Toutes':
        df_filtered = df_filtered[df_filtered['Saison'] == saison_selectionnee]
    if position_selectionnee != 'Toutes':
        df_filtered = df_filtered[df_filtered['Position'] == position_selectionnee]

# PAGE 1: TABLEAU DE BORD
if page == "🏠 Tableau de Bord":
    st.markdown("## 🏠 Tableau de Bord Général")
    
    # KPIs principaux
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">{}</div>
                <div class="stat-label">Joueurs Total</div>
            </div>
        """.format(df_filtered['Name'].nunique()), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">{}</div>
                <div class="stat-label">Buts Marqués</div>
            </div>
        """.format(int(df_filtered['Buts'].sum())), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">{}</div>
                <div class="stat-label">Passes Décisives</div>
            </div>
        """.format(int(df_filtered['Passes décisives'].sum())), unsafe_allow_html=True)
    
    with col4:
        valeur_totale = df_filtered['market_value'].sum() / 1000000
        st.markdown("""
            <div class="stat-box">
                <div class="stat-number">{:.1f}M€</div>
                <div class="stat-label">Valeur Totale</div>
            </div>
        """.format(valeur_totale), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution par position
        pos_counts = df_filtered['Position'].value_counts().reset_index()
        pos_counts.columns = ['Position', 'count']
        
        fig_positions = px.pie(
            pos_counts,
            values='count',
            names='Position',
            title="Répartition des Joueurs par Position",
            color_discrete_sequence=px.colors.sequential.Reds
        )
        fig_positions.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_positions, use_container_width=True)
    
    with col2:
        # Distribution des âges
        fig_ages = px.histogram(
            df_filtered,
            x='Age',
            title="Distribution des Âges",
            nbins=15,
            color_discrete_sequence=['#E61717']
        )
        fig_ages.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Âge",
            yaxis_title="Nombre de joueurs",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_ages, use_container_width=True)
    
    # Évolution par saison
    st.markdown("### 📈 Évolution par Saison")
    
    evol_saison = df.groupby('Saison').agg({
        'Buts': 'sum',
        'Passes décisives': 'sum',
        'Minutes jouées': 'sum'
    }).reset_index()
    
    fig_evolution = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Buts', 'Passes Décisives', 'Minutes Jouées')
    )
    
    fig_evolution.add_trace(
        go.Bar(x=evol_saison['Saison'], y=evol_saison['Buts'], 
               marker_color='#E61717', name='Buts'),
        row=1, col=1
    )
    
    fig_evolution.add_trace(
        go.Bar(x=evol_saison['Saison'], y=evol_saison['Passes décisives'], 
               marker_color='#D4AF37', name='Passes'),
        row=1, col=2
    )
    
    fig_evolution.add_trace(
        go.Bar(x=evol_saison['Saison'], y=evol_saison['Minutes jouées'], 
               marker_color='#1A1A1A', name='Minutes'),
        row=1, col=3
    )
    
    fig_evolution.update_layout(
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Poppins'}
    )
    
    # Update des couleurs des barres
    fig_evolution.data[0].marker.color = '#E61717' # Buts
    fig_evolution.data[1].marker.color = '#D4AF37' # Passes
    fig_evolution.data[2].marker.color = '#1A1A1A' # Minutes

    st.plotly_chart(fig_evolution, use_container_width=True)

# PAGE 2: PERFORMANCES
elif page == "📈 Performances":
    st.markdown("## 📈 Analyses de Performances")
    
    tab1, tab2, tab3 = st.tabs(["⚽ Attaque", "🛡️ Défense", "⏱️ Temps de Jeu"])
    
    with tab1:
        st.markdown("### ⚽ Top Buteurs")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            top_buteurs = df_filtered.groupby('Name').agg({
                'Buts': 'sum',
                'Matchs': 'sum',
                'Position': 'first'
            }).sort_values('Buts', ascending=False).head(10).reset_index()
            
            fig_buteurs = px.bar(
                top_buteurs,
                x='Buts',
                y='Name',
                orientation='h',
                title="Top 10 Buteurs",
                color='Buts',
                color_continuous_scale=['#FFD700', '#E61717', '#800000']
            )
            fig_buteurs.update_layout(height=500)
            st.plotly_chart(fig_buteurs, use_container_width=True)
        
        with col2:
            st.markdown("#### 🏆 Meilleurs Contributions")
            top_contrib = df_filtered.nlargest(5, 'Contributions_offensives')[
                ['Name', 'Buts', 'Passes décisives', 'Contributions_offensives']
            ]
            st.dataframe(
                top_contrib,
                hide_index=True,
                use_container_width=True,
                height=400
            )
    
    with tab2:
        st.markdown("### 🛡️ Discipline")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cartons par position
            cartons_pos = df_filtered.groupby('Position').agg({
                'Cartons Jaunes': 'sum',
                'CartonS rouges': 'sum'
            }).reset_index()
            
            fig_cartons = go.Figure()
            fig_cartons.add_trace(go.Bar(
                name='Cartons Jaunes',
                x=cartons_pos['Position'],
                y=cartons_pos['Cartons Jaunes'],
                marker_color='#FFD700'
            ))
            fig_cartons.add_trace(go.Bar(
                name='Cartons Rouges',
                x=cartons_pos['Position'],
                y=cartons_pos['CartonS rouges'],
                marker_color='#DC143C'
            ))
            fig_cartons.update_layout(
                title="Cartons par Position",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_cartons, use_container_width=True)
        
        with col2:
            # Joueurs les plus sanctionnés
            st.markdown("#### 🟨🟥 Joueurs les Plus Sanctionnés")
            
            cols_cartons = ['Name', 'Cartons Jaunes', 'CartonS rouges', 'Cartons_total']
            if saison_selectionnee == 'Toutes':
                cols_cartons.append('Saison')
                
            top_cartons = df_filtered.nlargest(10, 'Cartons_total')[cols_cartons]
            st.dataframe(top_cartons, hide_index=True, use_container_width=True)
    
    with tab3:
        st.markdown("### ⏱️ Temps de Jeu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Minutes par position
            minutes_pos = df_filtered.groupby('Position')['Minutes jouées'].sum().reset_index()
            
            fig_minutes = px.pie(
                minutes_pos,
                values='Minutes jouées',
                names='Position',
                title="Répartition des Minutes par Position",
                color_discrete_sequence=px.colors.sequential.Reds
            )
            st.plotly_chart(fig_minutes, use_container_width=True)
        
        with col2:
            # Top temps de jeu
            st.markdown("#### 🏃 Plus Gros Temps de Jeu")
            
            cols_minutes = ['Name', 'Position', 'Matchs', 'Minutes jouées', 'Minutes_par_match']
            if saison_selectionnee == 'Toutes':
                cols_minutes.append('Saison')
                
            top_minutes = df_filtered.nlargest(10, 'Minutes jouées')[cols_minutes]
            st.dataframe(
                top_minutes.round(1),
                hide_index=True,
                use_container_width=True
            )

# PAGE 3: JOUEURS
elif page == "👥 Joueurs":
    st.markdown("## 👥 Profils des Joueurs")
    
    # Recherche de joueur
    st.markdown("### 🔍 Rechercher un Joueur")
    joueur_recherche = st.selectbox(
        "Sélectionner un joueur",
        sorted(df['Name'].unique())
    )
    
    if joueur_recherche:
        joueur_data = df[df['Name'] == joueur_recherche]
        
        # Informations du joueur
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculs de carrière
        nb_saisons_joueur = joueur_data['Saison'].nunique()
        saisons_jouees = sorted(joueur_data['Saison'].unique().tolist())
        periode = f"{saisons_jouees[0]} - {saisons_jouees[-1]}" if len(saisons_jouees) > 1 else saisons_jouees[0]

        with col1:
            st.metric("Saisons Disputées", f"{nb_saisons_joueur}")
            st.caption(f"Période: {periode}")
        with col2:
            st.metric("Position", joueur_data['Position'].mode()[0] if len(joueur_data['Position'].mode()) > 0 else "N/A")
        with col3:
             total_buts = int(joueur_data['Buts'].sum())
             meilleure_saison_buts = joueur_data.loc[joueur_data['Buts'].idxmax(), 'Saison'] if total_buts > 0 else "-"
             st.metric("Total Buts", total_buts)
             if total_buts > 0:
                 st.caption(f"Meilleure saison: {meilleure_saison_buts}")
        with col4:
            st.metric("Total Passes", int(joueur_data['Passes décisives'].sum()))
        
        # Statistiques détaillées
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Statistiques par Saison")
            stats_saison = joueur_data.groupby('Saison').agg({
                'Matchs': 'sum',
                'Buts': 'sum',
                'Passes décisives': 'sum',
                'Minutes jouées': 'sum',
                'Cartons Jaunes': 'sum'
            }).reset_index()
            
            st.dataframe(stats_saison, hide_index=True, use_container_width=True)
        
        with col2:
            # Graphique d'évolution
            fig_joueur = go.Figure()
            fig_joueur.add_trace(go.Scatter(
                x=stats_saison['Saison'],
                y=stats_saison['Buts'],
                mode='lines+markers',
                name='Buts',
                line=dict(color='#DC143C', width=3)
            ))
            fig_joueur.add_trace(go.Scatter(
                x=stats_saison['Saison'],
                y=stats_saison['Passes décisives'],
                mode='lines+markers',
                name='Passes',
                line=dict(color='#B22222', width=3)
            ))
            
            # Ajout de la courbe PPM (Points Per Match) s'il y a des données dispos
            if 'PPM' in joueur_data.columns and not joueur_data['PPM'].isna().all():
                 # Calculer la moyenne de PPM par saison pour ce joueur
                 ppm_saison = joueur_data.groupby('Saison')['PPM'].mean().reset_index()
                 fig_joueur.add_trace(go.Scatter(
                    x=ppm_saison['Saison'],
                    y=ppm_saison['PPM'],
                    mode='lines+markers',
                    name='PPM (Moy.)',
                    line=dict(color='#1f77b4', width=2, dash='dot'),
                    yaxis='y2'
                ))
            
            fig_joueur.update_layout(
                title="Évolution des Performances (Buts, Passes & PPM)",
                height=400,
                yaxis=dict(title="Buts / Passes"),
                yaxis2=dict(
                    title="PPM",
                    overlaying="y",
                    side="right",
                    range=[0, 3]
                ),
                legend=dict(x=0, y=1.2, orientation="h")
            )
            st.plotly_chart(fig_joueur, use_container_width=True)
    
    st.markdown("---")
    
    # Comparaison de joueurs
    st.markdown("### 🔀 Comparaison de Joueurs")
    
    col1, col2 = st.columns(2)
    with col1:
        joueur1 = st.selectbox("Joueur 1", sorted(df['Name'].unique()), key='j1')
    with col2:
        joueur2 = st.selectbox("Joueur 2", sorted(df['Name'].unique()), key='j2')
    
    if joueur1 and joueur2:
        data_j1 = df[df['Name'] == joueur1].agg({
            'Buts': 'sum',
            'Passes décisives': 'sum',
            'Matchs': 'sum',
            'Minutes jouées': 'sum',
            'Cartons Jaunes': 'sum'
        })
        
        data_j2 = df[df['Name'] == joueur2].agg({
            'Buts': 'sum',
            'Passes décisives': 'sum',
            'Matchs': 'sum',
            'Minutes jouées': 'sum',
            'Cartons Jaunes': 'sum'
        })
        
        # Radar chart
        categories = ['Buts', 'Passes', 'Matchs', 'Minutes/100', 'Cartons']
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[data_j1['Buts'], data_j1['Passes décisives'], data_j1['Matchs'], 
               data_j1['Minutes jouées']/100, data_j1['Cartons Jaunes']],
            theta=categories,
            fill='toself',
            name=joueur1,
            line_color='#DC143C'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=[data_j2['Buts'], data_j2['Passes décisives'], data_j2['Matchs'], 
               data_j2['Minutes jouées']/100, data_j2['Cartons Jaunes']],
            theta=categories,
            fill='toself',
            name=joueur2,
            line_color='#4169E1'
        ))
        
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

# PAGE 4: VALEUR MARCHANDE
elif page == "💰 Valeur Marchande":
    st.markdown("## 💰 Analyse de la Valeur Marchande")
    
    # KPIs financiers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valeur_totale = df_filtered['market_value'].sum()
        st.metric("Valeur Totale", f"{valeur_totale/1000000:.1f}M€")
    
    with col2:
        valeur_moyenne = df_filtered['market_value'].mean()
        st.metric("Valeur Moyenne", f"{valeur_moyenne/1000:.0f}K€")
    
    with col3:
        if df_filtered['market_value'].max() > 0:
            joueur_plus_cher = df_filtered.loc[df_filtered['market_value'].idxmax(), 'Name']
            st.metric("Joueur le Plus Cher", joueur_plus_cher)
        else:
            st.metric("Joueur le Plus Cher", "N/A")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 joueurs les plus chers
        top_valeur = df_filtered.nlargest(10, 'market_value')[['Name', 'market_value', 'Position']]
        
        fig_valeur = px.bar(
            top_valeur,
            x='market_value',
            y='Name',
            orientation='h',
            title="Top 10 Joueurs par Valeur Marchande",
            color='market_value',
            color_continuous_scale=['#FFB6C1', '#DC143C', '#8B0000'],
            labels={'market_value': 'Valeur (€)'}
        )
        fig_valeur.update_layout(height=500)
        st.plotly_chart(fig_valeur, use_container_width=True)
    
    with col2:
        # Valeur par position
        valeur_pos = df_filtered.groupby('Position')['market_value'].agg(['sum', 'mean', 'count']).reset_index()
        
        fig_val_pos = px.bar(
            valeur_pos,
            x='Position',
            y='sum',
            title="Valeur Totale par Position",
            color='mean',
            color_continuous_scale='Reds',
            labels={'sum': 'Valeur Totale (€)', 'mean': 'Valeur Moyenne'}
        )
        fig_val_pos.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig_val_pos, use_container_width=True)
    
    # Évolution de la valeur
    st.markdown("### 📈 Évolution de la Valeur par Saison")
    
    valeur_saison = df.groupby('Saison')['market_value'].agg(['sum', 'mean']).reset_index()
    
    fig_evol_val = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_evol_val.add_trace(
        go.Bar(name="Valeur Totale", x=valeur_saison['Saison'], y=valeur_saison['sum'], 
               marker_color='#DC143C'),
        secondary_y=False,
    )
    
    fig_evol_val.add_trace(
        go.Scatter(name="Valeur Moyenne", x=valeur_saison['Saison'], y=valeur_saison['mean'], 
                   line=dict(color='#4169E1', width=3)),
        secondary_y=True,
    )
    
    fig_evol_val.update_layout(height=400)
    fig_evol_val.update_xaxes(title_text="Saison")
    fig_evol_val.update_yaxes(title_text="Valeur Totale (€)", secondary_y=False)
    fig_evol_val.update_yaxes(title_text="Valeur Moyenne (€)", secondary_y=True)
    
    st.plotly_chart(fig_evol_val, use_container_width=True)

# PAGE 5: ANALYSES AVANCÉES
elif page == "📊 Analyses Avancées":
    st.markdown("## 📊 Analyses Statistiques Avancées")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Efficacité", "📊 Corrélations", "🏆 Records", "🦁 Fidélité & Longévité"])
    
    with tab4:
        st.markdown("### 🦁 Fidélité & Longévité du Vestiaire")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Joueurs avec le plus de saisons
            st.markdown("#### 📅 Joueurs les plus Fidèles")
            nb_saisons = df_filtered.groupby('Name')['Saison'].nunique().sort_values(ascending=False).reset_index()
            nb_saisons.columns = ['Joueur', 'Nombre de Saisons']
            
            fig_saisons = px.bar(
                nb_saisons.head(15),
                x='Nombre de Saisons',
                y='Joueur',
                orientation='h',
                title="Top 15: Nombre de Saisons Disputées",
                color='Nombre de Saisons',
                color_continuous_scale=['#FFB6C1', '#DC143C', '#8B0000']
            )
            fig_saisons.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_saisons, use_container_width=True)

        with col2:
             # Heatmap de présence
            st.markdown("#### 🗓️ Présence par Saison (Top 20 Joueurs)")
            
            # On prend les 20 joueurs ayant le plus de matchs au total
            top_joueurs_matchs = df_filtered.groupby('Name')['Matchs'].sum().nlargest(20).index.tolist()
            presences = df_filtered[df_filtered['Name'].isin(top_joueurs_matchs)].pivot_table(
                index='Name', 
                columns='Saison', 
                values='Matchs', 
                aggfunc='sum'
            ).fillna(0)
            
            fig_heatmap = px.imshow(
                presences,
                labels=dict(x="Saison", y="Joueur", color="Matchs Joués"),
                x=presences.columns,
                y=presences.index,
                color_continuous_scale='Reds',
                aspect="auto"
            )
            fig_heatmap.update_layout(height=500, title="Matchs joués par saison")
            st.plotly_chart(fig_heatmap, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔄 Stabilité de l'Effectif")
        
        # Calcul de la rétention d'une année sur l'autre
        saisons_list = sorted(df['Saison'].unique())
        retention_data = []
        
        for i in range(len(saisons_list) - 1):
            s1 = saisons_list[i]
            s2 = saisons_list[i+1]
            joueurs_s1 = set(df[df['Saison'] == s1]['Name'])
            joueurs_s2 = set(df[df['Saison'] == s2]['Name'])
            
            communs = joueurs_s1.intersection(joueurs_s2)
            taux = len(communs) / len(joueurs_s1) * 100 if len(joueurs_s1) > 0 else 0
            
            retention_data.append({
                'Saison': f"{s1} → {s2}",
                'Taux de Rétention (%)': taux,
                'Joueurs Conservés': len(communs),
                'Effectif Saison N': len(joueurs_s1)
            })
            
        df_retention = pd.DataFrame(retention_data)
        
        fig_retention = px.line(
            df_retention, 
            x='Saison', 
            y='Taux de Rétention (%)',
            markers=True,
            title="Taux de Rétention de l'Effectif (Saison N par rapport à N+1)",
            line_shape='spline'
        )
        fig_retention.update_traces(line_color='#DC143C', line_width=4)
        fig_retention.update_layout(height=400, yaxis_range=[0, 100])
        st.plotly_chart(fig_retention, use_container_width=True)


    with tab1:
        st.markdown("### 🎯 Efficacité des Joueurs")
        
        # Calculer les métriques d'efficacité
        efficacite = df_filtered.groupby('Name').agg({
            'Buts': 'sum',
            'Matchs': 'sum',
            'Minutes jouées': 'sum',
            'Passes décisives': 'sum',
            'Position': 'first'
        }).reset_index()
        
        efficacite['Buts_par_match'] = efficacite['Buts'] / efficacite['Matchs']
        efficacite['Minutes_par_but'] = efficacite['Minutes jouées'] / efficacite['Buts'].replace(0, np.nan)
        efficacite['Contributions_par_match'] = (efficacite['Buts'] + efficacite['Passes décisives']) / efficacite['Matchs']
        
        # Scatter plot
        fig_efficacite = px.scatter(
            efficacite[efficacite['Matchs'] >= 5],
            x='Minutes jouées',
            y='Contributions_par_match',
            size='Buts',
            color='Position',
            hover_data=['Name'],
            title="Efficacité: Contributions vs Temps de Jeu (Min 5 matchs)",
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig_efficacite.update_layout(height=500)
        st.plotly_chart(fig_efficacite, use_container_width=True)
        
        # Top efficacité
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Meilleur Ratio Buts/Match")
            top_ratio = efficacite[efficacite['Matchs'] >= 5].nlargest(10, 'Buts_par_match')[
                ['Name', 'Position', 'Buts', 'Matchs', 'Buts_par_match']
            ]
            st.dataframe(top_ratio.round(3), hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### ⚡ Meilleur Ratio Minutes/But")
            top_min_but = efficacite[efficacite['Buts'] > 0].nsmallest(10, 'Minutes_par_but')[
                ['Name', 'Position', 'Buts', 'Minutes_par_but']
            ]
            st.dataframe(top_min_but.round(0), hide_index=True, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Analyse des Corrélations")
        
        # Matrice de corrélation
        numeric_cols = ['Age', 'Matchs', 'Buts', 'Passes décisives', 'Minutes jouées', 
                       'Cartons Jaunes', 'PPM', 'market_value']
        
        # Vérifier que les colonnes existent
        available_cols = [col for col in numeric_cols if col in df_filtered.columns]
        
        corr_matrix = df_filtered[available_cols].corr()
        
        fig_corr = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect="auto",
            title="Matrice de Corrélation",
            color_continuous_scale='RdYlBu_r'
        )
        fig_corr.update_layout(height=600)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Insights
        st.markdown("#### 💡 Insights Clés")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'Buts' in corr_matrix.index and 'Minutes jouées' in corr_matrix.columns:
                corr_buts_minutes = corr_matrix.loc['Buts', 'Minutes jouées']
                st.metric("Corrélation Buts - Minutes", f"{corr_buts_minutes:.2f}")
        
        with col2:
            if 'Age' in corr_matrix.index and 'market_value' in corr_matrix.columns:
                corr_age_valeur = corr_matrix.loc['Age', 'market_value']
                st.metric("Corrélation Âge - Valeur", f"{corr_age_valeur:.2f}")
        
        with col3:
            if 'Buts' in corr_matrix.index and 'market_value' in corr_matrix.columns:
                corr_buts_valeur = corr_matrix.loc['Buts', 'market_value']
                st.metric("Corrélation Buts - Valeur", f"{corr_buts_valeur:.2f}")
    
    with tab3:
        st.markdown("### 🏆 Records et Statistiques Remarquables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌟 Records Individuels")
            
            records = {
                "🥇 Plus de buts en une saison": int(df.groupby(['Name', 'Saison'])['Buts'].sum().max()),
                "🎯 Plus de passes en une saison": int(df.groupby(['Name', 'Saison'])['Passes décisives'].sum().max()),
                "⏱️ Plus de minutes en une saison": int(df.groupby(['Name', 'Saison'])['Minutes jouées'].sum().max()),
                "🟨 Plus de cartons jaunes": int(df['Cartons Jaunes'].max()),
                "💰 Valeur la plus élevée": f"{df['market_value'].max()/1000:.0f}K€"
            }
            
            for record, valeur in records.items():
                st.markdown(f"**{record}**: {valeur}")
        
        with col2:
            st.markdown("#### 📈 Statistiques d'Équipe")
            
            stats_equipe = {
                "👥 Total de joueurs différents": df['Name'].nunique(),
                "⚽ Total de buts marqués": int(df['Buts'].sum()),
                "🎯 Total de passes décisives": int(df['Passes décisives'].sum()),
                "⏱️ Total de minutes jouées": f"{int(df['Minutes jouées'].sum()/60000)}K heures",
                "🎂 Âge moyen": f"{df['Age'].mean():.1f} ans"
            }
            
            for stat, valeur in stats_equipe.items():
                st.markdown(f"**{stat}**: {valeur}")
        
        # Meilleurs par catégorie
        st.markdown("#### 🏅 Hall of Fame")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🥇 Top Buteur All-Time**")
            top_buteur = df.groupby('Name')['Buts'].sum().idxmax()
            buts_total = df.groupby('Name')['Buts'].sum().max()
            st.success(f"{top_buteur}\n\n{int(buts_total)} buts")
        
        with col2:
            st.markdown("**🎯 Top Passeur All-Time**")
            top_passeur = df.groupby('Name')['Passes décisives'].sum().idxmax()
            passes_total = df.groupby('Name')['Passes décisives'].sum().max()
            st.success(f"{top_passeur}\n\n{int(passes_total)} passes")
        
        with col3:
            st.markdown("**⏱️ Plus de Temps de Jeu**")
            top_minutes = df.groupby('Name')['Minutes jouées'].sum().idxmax()
            minutes_total = df.groupby('Name')['Minutes jouées'].sum().max()
            st.success(f"{top_minutes}\n\n{int(minutes_total)} minutes")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p><strong>Wydad Athletic Club</strong> - Analyse Statistique Professionnelle</p>
        <p>🔴⚪ DiMa Wydad - Fondé en 1937</p>
        <p>Créé avec ❤️</p>
    </div>
""", unsafe_allow_html=True)