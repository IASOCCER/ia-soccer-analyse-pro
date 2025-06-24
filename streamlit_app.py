import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer – Analyse de Passe", layout="wide")
st.title("🎯 IA Soccer – Analyse de Passe – Série Complète")

# Initialisation
if "passe_series" not in st.session_state:
    st.session_state["passe_series"] = []
if "passe_temp" not in st.session_state:
    st.session_state["passe_temp"] = []

# 🔍 IA – Analyse finale
def analyse_serie(passes, age, pression):
    total = len(passes)
    reussis = sum(1 for p in passes if p["Réussi"] == "Oui")
    precision = (reussis / total) * 100
    temps_moyen = sum(p["Temps (s)"] for p in passes) / total

    plan = []

    if precision >= 80:
        note = "Excellent"
        plan.append("🟢 Passes précises, maintenir la constance sous pression.")
    elif precision >= 50:
        note = "Moyen"
        plan.append("🟠 Travailler la stabilité du geste et la vitesse d'exécution.")
    else:
        note = "À améliorer"
        plan.append("🔴 Répétitions ciblées sur des passes simples avec corrections vidéo.")

    if pression == 3:
        plan.append("🔥 Réagir rapidement à des stimuli visuels dans des jeux réduits (3v3).")
    elif pression == 6:
        plan.append("💨 Travailler en binôme avec pression simulée (2 secondes max).")
    else:
        plan.append("🧊 Stabiliser la technique sans contrainte de temps.")

    if age < 12:
        plan.append("🎯 Jeux avec Blazepod pour améliorer les réflexes.")
    else:
        plan.append("🧠 Ajouter la prise de décision dans le choix du type de passe.")

    return precision, temps_moyen, note, " • ".join(plan)

# 👤 Informations du joueur
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)
pression = st.selectbox("Niveau de pression", ["Sans pression (12s)", "Pression moyenne (6s)", "Haute pression (3s)"])
pression_val = {"Sans pression (12s)": 12, "Pression moyenne (6s)": 6, "Haute pression (3s)": 3}[pression]

# ➕ Ajouter un passe
st.markdown("### ➕ Ajouter chaque passe")
cible = st.selectbox("Cible visée", [1, 2, 3, 4, 5, 6])
temps = st.number_input("Temps de réaction (en secondes)", min_value=0.0, step=0.01)
reussi = st.radio("Passe réussie ?", ["Oui", "Non"])

if st.button("Ajouter ce passe"):
    st.session_state["passe_temp"].append({
        "Cible": cible,
        "Temps (s)": temps,
        "Réussi": reussi
    })

# 📋 Tableau temporaire
if st.session_state["passe_temp"]:
    st.markdown("### 📌 Passes enregistrées")
    st.dataframe(pd.DataFrame(st.session_state["passe_temp"]), use_container_width=True)

# ✅ Finaliser la série
if st.button("✅ Finaliser la série"):
    if nom and len(st.session_state["passe_temp"]) == 6:
        precision, temps_moyen, note, plan = analyse_serie(
            st.session_state["passe_temp"], age, pression_val
        )
        st.session_state["passe_series"].append({
            "Nom": nom,
            "Âge": age,
            "Pression": pression,
            "Précision (%)": round(precision, 1),
            "Temps moyen (s)": round(temps_moyen, 2),
            "Note": note,
            "Plan d'action": plan
        })
        st.session_state["passe_temp"] = []
    else:
        st.warning("Veuillez entrer un nom et enregistrer exactement 6 passes.")

# 📊 Résultats finaux
if st.session_state["passe_series"]:
    st.markdown("### 📊 Séries de passe complètes")
    df = pd.DataFrame(st.session_state["passe_series"])
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger (.csv)", csv, "series_passe.csv", "text/csv")



