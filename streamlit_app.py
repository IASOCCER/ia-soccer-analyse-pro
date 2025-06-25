import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.sidebar.image("https://iasoccer.com/wp-content/uploads/2024/09/IA-SOCCER-FC-PORTO-WHITE.png", width=250)
st.sidebar.title("IA Soccer Analyse Pro")

# Menu lateral
page = st.sidebar.selectbox("Choisissez une section :", [
    "🏠 Accueil",
    "🧍 Informations du joueur",
    "🎯 Test de Passe",
    "📊 Rapport Global"
])

# Base de dados temporária
if "joueur" not in st.session_state:
    st.session_state["joueur"] = {}

if "passe_tests" not in st.session_state:
    st.session_state["passe_tests"] = []

# Função para análise automática
def analyser_passe(test):
    precision = test["précision"]
    temps_moyen = test["temps_moyen"]

    # Notas baseadas em precisão e tempo
    if precision >= 80 and temps_moyen <= 3:
        note = "Excellent"
        plan = "Maintenir l'entraînement actuel. Ajouter des passes en mouvement."
    elif precision >= 60:
        note = "Bon"
        plan = "Améliorer la vitesse d'exécution. Travailler la précision sous pression."
    else:
        note = "À améliorer"
        plan = "Focaliser sur la technique de passe. Réduire le temps de réaction."

    return note, plan

# ACCUEIL
if page == "🏠 Accueil":
    st.title("Bienvenue à IA Soccer Analyse Pro ⚽")
    st.markdown("Cette plateforme permet d'évaluer la performance technique et physique des joueurs de 8 à 18 ans.")
    st.markdown("Utilisez le menu à gauche pour naviguer entre les tests.")
    st.info("🔐 Le système est en version test. Le stockage dans Google Drive sera activé dans les prochaines étapes.")

# INFOS JOUEUR
elif page == "🧍 Informations du joueur":
    st.title("🧍 Informations du joueur")
    nom = st.text_input("Nom complet")
    age = st.number_input("Âge", min_value=8, max_value=18)
    categorie = st.selectbox("Catégorie", ["U8", "U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U17", "U18"])
    position = st.selectbox("Position", ["Gardien", "Défenseur", "Milieu", "Attaquant"])

    if st.button("✅ Sauvegarder les informations"):
        st.session_state["joueur"] = {
            "nom": nom,
            "âge": age,
            "catégorie": categorie,
            "position": position
        }
        st.success("Informations du joueur sauvegardées.")

# TEST DE PASSE
elif page == "🎯 Test de Passe":
    st.title("🎯 Test de Passe – Analyse avec IA")

    if not st.session_state["joueur"]:
        st.warning("Veuillez d'abord remplir les informations du joueur.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            precision = st.slider("🎯 Précision (%)", 0, 100, 50)
        with col2:
            temps = st.number_input("⏱️ Temps moyen (secondes)", min_value=0.0, step=0.1)

        pied = st.selectbox("🦶 Pied utilisé", ["Droit", "Gauche"])
        pression = st.selectbox("💥 Niveau de pression", ["Faible", "Moyenne", "Élevée"])

        if st.button("➕ Ajouter ce test"):
            test = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "précision": precision,
                "temps_moyen": temps,
                "pied": pied,
                "pression": pression
            }
            note, plan = analyser_passe(test)
            test["note"] = note
            test["plan_action"] = plan
            st.session_state["passe_tests"].append(test)
            st.success("Test ajouté.")

        if st.session_state["passe_tests"]:
            st.markdown("### 📄 Résumé des tests de passe")
            df = pd.DataFrame(st.session_state["passe_tests"])
            st.dataframe(df)

            if st.button("📤 Exporter vers fichier CSV"):
                joueur = st.session_state["joueur"]
                filename = f"{joueur['nom'].replace(' ', '_')}_passe.csv"
                df.to_csv(filename, index=False)
                st.success(f"Fichier sauvegardé : {filename}")

# RAPPORT GLOBAL
elif page == "📊 Rapport Global":
    st.title("📊 Rapport Global")
    st.markdown("⚠️ Cette section affichera bientôt tous les tests et générera un rapport automatique avec IA.")
    st.warning("Encore en construction. Revenez bientôt !")










