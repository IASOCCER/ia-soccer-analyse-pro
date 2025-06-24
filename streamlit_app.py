import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer – Analyse de Passe", layout="wide")
st.title("🎯 IA Soccer – Analyse de Passe")

# Initialisation
if "passe_tests" not in st.session_state:
    st.session_state["passe_tests"] = []

# 🔍 Fonction IA – Évaluation + Plan d'action professionnel
def evaluer_passe(age, precision, pression):
    plan = []

    # Bloc 1 : Précision
    if precision >= 80:
        note = "Excellent"
        plan.append("🟢 Maintenir la régularité avec des passes sous pression en mouvement.")
        plan.append("🔁 Introduire des passes avec changements de direction rapides.")
    elif precision >= 50:
        note = "Moyen"
        plan.append("🟠 Améliorer la précision avec des séries de 10 passes fixes sur cible.")
        plan.append("👣 Corriger l'appui du pied non-dominant.")
    else:
        note = "À améliorer"
        plan.append("🔴 Répéter des passes à courte distance avec corrections vidéo.")
        plan.append("👀 Travailler la posture et la prise d'information avant le geste.")

    # Bloc 2 : Pression
    if pression == 3:
        plan.append("🔥 Simuler des passes en situation de match à haute intensité (jeu réduit 3v3).")
    elif pression == 6:
        plan.append("💨 Répéter des passes avec adversaire fictif (pression moyenne, 2 secondes).")
    else:
        plan.append("🧊 Travailler la concentration et la technique sans contrainte de temps.")

    # Bloc 3 : Âge
    if age < 12:
        plan.append("🎯 Jeux ludiques avec Blazepods pour stimuler les réflexes.")
    else:
        plan.append("🧠 Ajouter la prise de décision: passer ou conduire selon la situation.")

    return note, " • ".join(plan)

# 👤 Informations du joueur
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)
pied = st.selectbox("Pied utilisé", ["Droit", "Gauche"])
pression = st.selectbox("Pression", ["Sans pression (12s)", "Pression moyenne (6s)", "Haute pression (3s)"])
pression_val = {"Sans pression (12s)": 12, "Pression moyenne (6s)": 6, "Haute pression (3s)": 3}[pression]

# 🎯 Résultats du test
st.markdown("### 🎯 Résultats du test")
cibles_total = 6
cibles_reussies = st.number_input("Cibles touchées (sur 6)", min_value=0, max_value=6, step=1)

# ➕ Ajouter le test
if st.button("➕ Ajouter ce test"):
    if nom:
        precision = (cibles_reussies / cibles_total) * 100
        note, plan = evaluer_passe(age, precision, pression_val)
        st.session_state["passe_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Pied": pied,
            "Pression": pression,
            "Cibles réussies": cibles_reussies,
            "Précision (%)": round(precision, 1),
            "Note": note,
            "Plan d'action professionnel": plan
        })
    else:
        st.warning("Veuillez entrer le nom du joueur.")

# 📊 Résultats enregistrés
if st.session_state["passe_tests"]:
    st.markdown("### 📊 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["passe_tests"])
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger (.csv)", csv, "passe_tests.csv", "text/csv")



