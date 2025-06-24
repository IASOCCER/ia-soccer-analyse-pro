import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")

# Menu lateral
menu = st.sidebar.selectbox("Choisissez un test", [
    "🏁 Accueil",
    "🎯 Test de Passe",
    "⚡ Conduite de Balle – Zig-Zag",
    "🌀 Conduite de Balle – Circuit"
])

st.title("⚽ IA Soccer – Analyse Technique")

# Página inicial
if menu == "🏁 Accueil":
    st.markdown("""
        ## Bienvenue sur la plateforme IA Soccer Analyse Pro
        Sélectionnez un test dans le menu à gauche pour commencer l'évaluation technique des joueurs.
    """)

# 🎯 TESTE DE PASSE
elif menu == "🎯 Test de Passe":
    if "tests_passe" not in st.session_state:
        st.session_state["tests_passe"] = []

    st.header("🎯 Analyse de Passe")
    nom = st.text_input("Nom du joueur", key="nom_passe")
    age = st.number_input("Âge", 8, 18, key="age_passe")
    pied = st.selectbox("Pied utilisé", ["Pied gauche", "Pied droit"], key="pied_passe")
    pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"], key="pression_passe")
    nb_acertes = st.slider("Nombre de passes réussies sur 6", 0, 6, 3, key="nb_passe")

    temps_reactions = []
    if nb_acertes > 0:
        st.markdown("Temps pour chaque passe réussie :")
        for i in range(1, nb_acertes + 1):
            t = st.number_input(f"Temps pour la passe {i}", 0.0, 15.0, step=0.1, key=f"passe_{i}")
            temps_reactions.append(t)

    if st.button("➕ Ajouter ce test", key="ajouter_passe"):
        if nom and age:
            precision = round((nb_acertes / 6) * 100, 1)
            temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if temps_reactions else 0.0
            st.session_state["tests_passe"].append({
                "Nom": nom,
                "Âge": age,
                "Pied": pied,
                "Pression": pression,
                "Précision (%)": precision,
                "Temps moyen (s)": temps_moyen
            })
            st.success("✅ Test de passe ajouté.")
        else:
            st.warning("Veuillez remplir les champs du joueur.")

    if st.session_state["tests_passe"]:
        st.subheader("📊 Résultats des passes")
        df = pd.DataFrame(st.session_state["tests_passe"])
        st.dataframe(df)

# ⚡ CONDUÇÃO DE BOLA – ZIG-ZAG
elif menu == "⚡ Conduite de Balle – Zig-Zag":
    st.header("⚡ Conduite de Balle – Zig-Zag")

    nom = st.text_input("Nom du joueur", key="nom_zigzag")
    age = st.number_input("Âge", 8, 18, key="age_zigzag")
    poids = st.number_input("Poids (kg)", 20.0, 100.0, key="poids_zigzag")
    masse = st.selectbox("Masse musculaire", ["Faible", "Moyenne", "Élevée"], key="masse_zigzag")

    temps = st.number_input("Temps total (en secondes)", 0.0, 30.0, step=0.1, key="temps_zigzag")

    if st.button("➕ Ajouter ce test", key="ajouter_zigzag"):
        st.success(f"Test enregistré: {nom}, {age} ans, {temps}s")

# 🌀 CONDUÇÃO DE BOLA – CIRCUITO EM L
elif menu == "🌀 Conduite de Balle – Circuit":
    st.header("🌀 Conduite de Balle – Circuit en L")

    nom = st.text_input("Nom du joueur", key="nom_circuit")
    age = st.number_input("Âge", 8, 18, key="age_circuit")
    poids = st.number_input("Poids (kg)", 20.0, 100.0, key="poids_circuit")
    masse = st.selectbox("Masse musculaire", ["Faible", "Moyenne", "Élevée"], key="masse_circuit")

    temps = st.number_input("Temps total (en secondes)", 0.0, 30.0, step=0.1, key="temps_circuit")

    if st.button("➕ Ajouter ce test", key="ajouter_circuit"):
        st.success(f"Test enregistré: {nom}, {age} ans, {temps}s")


