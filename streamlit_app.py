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

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyse de Conduite de Balle – IA Soccer", layout="wide")
st.title("⚽ IA Soccer – Analyse de la Conduite de Balle")

if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

st.markdown("### 🧑‍🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)
poids = st.number_input("Poids (kg)", min_value=20.0, max_value=120.0, step=0.1)
musculature = st.selectbox("Niveau de masse musculaire", ["Faible", "Moyenne", "Élevée"])

st.markdown("### 🛠️ Type de test de conduite")
type_test = st.selectbox("Choisir le test de conduite", ["Zig-Zag (5 cônes, 3m)", "Circuit en L ou circulaire"])
temps = st.number_input("⏱️ Temps total du test (en secondes)", min_value=0.0, max_value=30.0, step=0.1)

if st.button("➕ Ajouter ce test"):
    if nom and age > 0:
        st.session_state["conduite_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Poids (kg)": poids,
            "Masse musculaire": musculature,
            "Type de test": type_test,
            "Temps (s)": temps
        })
        st.success("✅ Test ajouté avec succès!")
    else:
        st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

if st.session_state["conduite_tests"]:
    st.markdown("### 📊 Tests enregistrés")
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.dataframe(df, use_container_width=True)

    if st.button("📄 Générer le rapport de conduite"):
        st.markdown(f"### 📌 Rapport pour {nom}, {age} ans")

        for test_type in df["Type de test"].unique():
            sous_df = df[df["Type de test"] == test_type]
            if not sous_df.empty:
                st.markdown(f"#### 🛤️ {test_type}")
                st.dataframe(sous_df[["Temps (s)"]])

                temps_moyen = sous_df["Temps (s)"].mean()
                st.markdown(f"- **Temps moyen :** {temps_moyen:.2f} s")

                st.markdown("### 🧠 Analyse automatique")
                if temps_moyen < 6:
                    st.markdown("- ✅ **Excellente conduite** – rapidité et contrôle.")
                elif 6 <= temps_moyen <= 8:
                    st.markdown("- ⚠️ **Bonne conduite** – peut être optimisée.")
                else:
                    st.markdown("- ❌ **Conduite lente** – nécessite plus de fluidité.")

                st.markdown("### 🎯 Plan d'action recommandé")
                if temps_moyen > 8:
                    st.markdown("""
#### 🟥 Niveau Prioritaire – Amélioration urgente

**Objectif :** Augmenter la vitesse avec contrôle du ballon.  
**Exercices :**
- Slalom entre cônes avec changement de rythme
- Courses courtes avec conduite serrée
- Travail technique en espace réduit

**Fréquence :** 3 fois par semaine pendant 4 semaines
**Objectif :** Réduire sous 7s
                    """)
                elif 6 <= temps_moyen <= 8:
                    st.markdown("""
#### 🟨 Niveau Modéré – Consolidation

**Objectif :** Maintenir un bon niveau tout en gagnant en fluidité.  
**Exercices :**
- Conduite latérale + rotation
- Conduite + feintes
- Transitions attaque-défense avec ballon

**Fréquence :** 2 fois par semaine
**Objectif :** Stabiliser en dessous de 6.5s
                    """)
                else:
                    st.markdown("""
#### 🟩 Niveau Avancé – Perfectionnement

**Objectif :** Maintenir les performances sous pression de match.  
**Exercices :**
- Conduite sous pression (1v1)
- Conduite en vision périphérique
- Évaluation vidéo de la posture

**Fréquence :** 1 session spécifique par semaine
**Objectif :** Appliquer en situation réelle

