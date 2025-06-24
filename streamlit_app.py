import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer – Analyse Technique", layout="wide")
st.title("⚽ IA Soccer – Analyse Technique avec IA")

# Initialisation de la mémoire
if "passe_tests" not in st.session_state:
    st.session_state["passe_tests"] = []
if "remate_tests" not in st.session_state:
    st.session_state["remate_tests"] = []

menu = st.sidebar.selectbox("Choisissez le test :", [
    "🏷️ Informations du joueur",
    "🎯 Test de Passe",
    "🔥 Test de Remate"
])

if menu == "🏷️ Informations du joueur":
    st.markdown("### 👤 Informations sur le joueur")
    st.session_state["joueur_nom"] = st.text_input("Nom du joueur")
    st.session_state["joueur_age"] = st.number_input("Âge", min_value=8, max_value=18)
    st.session_state["joueur_masse"] = st.number_input("Masse corporelle (kg)", min_value=20.0, max_value=120.0, step=0.1)

elif menu == "🎯 Test de Passe":
    st.markdown("### 🎯 Analyse de Passe")
    pied = st.selectbox("Pied utilisé", ["Pied gauche", "Pied droit"])
    pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"])
    nb_acertes = st.slider("Nombre de passes réussies sur 6", 0, 6, 3)

    temps_reactions = []
    if nb_acertes > 0:
        st.markdown("Saisir les temps de réaction (en secondes) pour chaque passe réussie :")
        for i in range(1, nb_acertes + 1):
            t = st.number_input(f"Temps pour la passe {i}", min_value=0.0, max_value=15.0, step=0.1, key=f"passe_{i}")
            temps_reactions.append(t)

    if st.button("➕ Ajouter ce test de passe"):
        nom = st.session_state.get("joueur_nom", "")
        age = st.session_state.get("joueur_age", "")
        if nom and age:
            precision = round((nb_acertes / 6) * 100, 1)
            temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if nb_acertes > 0 else 0.0
            st.session_state["passe_tests"].append({
                "Nom": nom,
                "Âge": age,
                "Pied": pied,
                "Pression": pression,
                "Précision (%)": precision,
                "Temps moyen (s)": temps_moyen
            })
            st.success("✅ Test de passe ajouté avec succès!")
        else:
            st.warning("Veuillez d'abord remplir les informations du joueur dans le menu de gauche.")

    if st.session_state["passe_tests"]:
        st.markdown("### 📊 Résultats – Test de Passe")
        st.dataframe(pd.DataFrame(st.session_state["passe_tests"]))

elif menu == "🔥 Test de Remate":
    st.markdown("### 🔥 Analyse de Remate")
    nb_tirs = st.slider("Nombre de tirs effectués", 0, 10, 5)
    nb_cibles = st.slider("Nombre de cibles atteintes", 0, nb_tirs, 3)
    vitesse = st.number_input("Vitesse moyenne (km/h)", min_value=0.0, max_value=200.0, step=0.1)

    if st.button("➕ Ajouter ce test de remate"):
        nom = st.session_state.get("joueur_nom", "")
        age = st.session_state.get("joueur_age", "")
        if nom and age:
            precision = round((nb_cibles / nb_tirs) * 100, 1) if nb_tirs > 0 else 0.0
            st.session_state["remate_tests"].append({
                "Nom": nom,
                "Âge": age,
                "Tirs": nb_tirs,
                "Cibles": nb_cibles,
                "Précision (%)": precision,
                "Vitesse (km/h)": vitesse
            })
            st.success("✅ Test de remate ajouté avec succès!")
        else:
            st.warning("Veuillez d'abord remplir les informations du joueur dans le menu de gauche.")

    if st.session_state["remate_tests"]:
        st.markdown("### 📊 Résultats – Test de Remate")
        st.dataframe(pd.DataFrame(st.session_state["remate_tests"]))


