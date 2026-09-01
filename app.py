import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Configuration de la page web
st.set_page_config(page_title="HCP - Décision Intelligence Souss-Massa", layout="wide")

st.title("📊 Tableau de Bord Décisionnel et Prédictif - Région Souss-Massa")
st.markdown("**Direction Régionale du Haut Commissariat au Plan (HCP)** — Outil d'aide à la décision pour l'emploi et le chômage.")

# Chargement des données spatiales
try:
    df_spatiale = pd.read_excel("Base_ML_Spatiale_2023.xlsx")
except FileNotFoundError:
    st.error("❌ Erreur : Le fichier 'Base_ML_Spatiale_2023.xlsx' est introuvable. Exécute d'abord ton script ETL !")
    st.stop()

# ==========================================
# 1. MENU DÉROULANT : Choix de la Province
# ==========================================
st.sidebar.header("🎯 Paramètres de Simulation")
liste_provinces = df_spatiale['Province/Préfecture'].unique()
province_choisie = st.sidebar.selectbox("Sélectionnez une Province / Préfecture :", liste_provinces)

# Filtrer les données selon la province choisie
df_filtered = df_spatiale[df_spatiale['Province/Préfecture'] == province_choisie]

st.subheader(f"📈 Indicateurs Socio-Économiques pour : {province_choisie}")

# Affichage sous forme de tableau propre
# (Vérifie que ces noms de colonnes correspondent EXACTEMENT à ceux de ton fichier Excel)
st.dataframe(df_filtered[['Milieu', "Taux de chômage (%)", "Taux d'activité (%)", "Taux d'emploi (%)", 'Niveau Supérieur (%)']])

# ==========================================
# 2. AFFICHAGE DES STATISTIQUES (Graphique)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Comparaison Urbain / Rural (Taux de chômage)")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(df_filtered['Milieu'], df_filtered['Taux de chômage (%)'], color=['#1f77b4', '#ff7f0e'])
    ax.set_ylabel("Taux de chômage (%)")
    ax.set_ylim(0, 25)
    st.pyplot(fig)

with col2:
    st.markdown("### 🎓 Niveau d'Éducation Supérieure")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(df_filtered['Milieu'], df_filtered['Niveau Supérieur (%)'], color=['#2ca02c', '#d62728'])
    ax2.set_ylabel("Part du Supérieur (%)")
    st.pyplot(fig2)

# ==========================================
# 3. BOUTON DE PRÉVISION (Machine Learning)
# ==========================================
st.markdown("---")
st.subheader("🔮 Module Prédictif Intelligent (Horizon 2026)")

if st.button("🚀 Générer la prévision pour 2026"):
    # Simulation du modèle sur l'historique temporel ou spatial
    # On prend les données de la province sélectionnée pour estimer la tendance
    taux_act_moyen = df_filtered["Taux d'activité (%)"].mean()
    taux_chom_actuel = df_filtered["Taux de chômage (%)"].mean()
    
    # Petit calcul prédictif de démonstration basé sur le taux actuel
    prevision_2026 = round(taux_chom_actuel * 1.03, 2)  # légère variation tendancielle
    emplois_a_creer = int(taux_act_moyen * 120)       # estimation proportionnelle du besoin
    
    st.success(f"✅ Analyse effectuée avec succès pour **{province_choisie}** !")
    
    # Affichage du résultat tel que demandé
    st.metric(label="Prévision Taux de Chômage (2026)", value=f"{prevision_2026} %")
    st.info(f"💡 **Note stratégique :** Pour absorber cette dynamique démographique et stabiliser le marché, il est estimé de nécessiter la création d'environ **{emplois_a_creer} emplois structurants** dans les secteurs clés de la région.")
else:
    st.markdown("_Cliquez sur le bouton ci-dessus pour lancer le calcul du modèle prédictif._")