import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.title("⚽ IA Soccer Analyse Pro")

# Menu principal
menu = st.sidebar.radio("Choisir un test :", [
    "Informations du Joueur",
    "Test de Passe",
    "Test de Remate",
    "Test de Conduite de Balle",
    "Test d'Agilité",
    "Test de Réaction",
    "Test de Sprint"
])

# Initialisation des états
if "joueur" not in st.session_state:
    st.session_state.joueur = {}
if "tests" not in st.session_state:
    st.session_state.tests = {
        "passe": [],
        "remate": [],
        "conduite": [],
        "agilite": [],
        "reaction": [],
        "sprint": []
    }

# Section 1 : Informations du Joueur
if menu == "Informations du Joueur":
    st.subheader("👤 Informations sur le joueur")
    nom = st.text_input("Nom du joueur")
    age = st.number_input("Âge", min_value=8, max_value=18)
    poids = st.number_input("Poids (kg)", min_value=20.0, max_value=120.0, step=0.1)
    taille = st.number_input("Taille (cm)", min_value=100.0, max_value=210.0, step=0.1)

    if st.button("✅ Enregistrer les informations"):
        st.session_state.joueur = {
            "nom": nom,
            "age": age,
            "poids": poids,
            "taille": taille
        }
        st.success("Informations enregistrées avec succès.")

# Section 2 : Test de Passe
elif menu == "Test de Passe":
    st.subheader("🎯 Test de Passe")
    pied = st.selectbox("Pied utilisé", ["Pied gauche", "Pied droit"])
    pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"])
    nb_acertes = st.slider("Nombre de passes réussies sur 6", 0, 6, 3)
    temps_reactions = []

    if nb_acertes > 0:
        st.markdown("**Temps de réaction pour chaque passe réussie :**")
        for i in range(1, nb_acertes + 1):
            t = st.number_input(f"Temps pour la passe {i} (s)", min_value=0.0, max_value=15.0, step=0.1, key=f"passe_{i}")
            temps_reactions.append(t)

    if st.button("➕ Ajouter ce test", key="ajouter_passe"):
        precision = round((nb_acertes / 6) * 100, 1)
        temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if temps_reactions else 0.0
        st.session_state.tests["passe"].append({
            "Pied": pied,
            "Pression": pression,
            "Précision (%)": precision,
            "Temps moyen (s)": temps_moyen
        })
        st.success("Test de passe ajouté.")

    if st.session_state.tests["passe"]:
        st.dataframe(pd.DataFrame(st.session_state.tests["passe"]))

# Section 3 : Test de Remate
elif menu == "Test de Remate":
    st.subheader("🥅 Test de Remate")
    nb_tentatives = st.slider("Nombre de remates", 1, 20, 10)
    nb_buts = st.slider("Nombre de buts (alvos touchés)", 0, nb_tentatives)
    vitesse_moyenne = st.number_input("Vitesse moyenne du tir (km/h)", min_value=0.0, max_value=150.0)

    if st.button("➕ Ajouter ce test", key="ajouter_remate"):
        precision = round((nb_buts / nb_tentatives) * 100, 1)
        st.session_state.tests["remate"].append({
            "Tirs": nb_tentatives,
            "Buts": nb_buts,
            "Précision (%)": precision,
            "Vitesse (km/h)": vitesse_moyenne
        })
        st.success("Test de remate ajouté.")

    if st.session_state.tests["remate"]:
        st.dataframe(pd.DataFrame(st.session_state.tests["remate"]))

# Les autres sections seront ajoutées de la même manière
elif menu == "Test de Conduite de Balle":
    st.subheader("🚶‍♂️ Test de Conduite de Balle")
    # À compléter selon le format souhaité

elif menu == "Test d'Agilité":
    st.subheader("🌀 Test d'Agilité")
    # À compléter selon le format souhaité

elif menu == "Test de Réaction":
    st.subheader("⚡ Test de Réaction")
    # À compléter selon le format souhaité

elif menu == "Test de Sprint":
    st.subheader("🏃‍♂️ Test de Sprint")
    # À compléter selon le format souhaité



