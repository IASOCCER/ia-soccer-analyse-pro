import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.title("⚽ IA Soccer – Analyse Technique")
st.sidebar.markdown("## 📋 Menu d’analyse")

# Menu latéral
test_selection = st.sidebar.selectbox(
    "Choisissez un test",
    ["Conduite", "Passe", "Remate", "Sprint", "Agilité", "Réaction"]
)

# Initialisation
if "tests" not in st.session_state:
    st.session_state["tests"] = {
        "Conduite": [],
        "Passe": [],
        "Remate": [],
        "Sprint": [],
        "Agilité": [],
        "Réaction": []
    }

def ajouter_resultat(categorie, data):
    st.session_state["tests"][categorie].append(data)

# 🔍 FONCTION IA – CONDUITE
def evaluer_conduite(age, temps):
    if age <= 9:
        if temps < 9:
            return "Excellent", "Poursuivre avec des parcours plus complexes"
        elif temps < 11:
            return "Bon", "Travailler la vitesse avec changements de direction"
        else:
            return "À améliorer", "Renforcer la coordination et agilité"
    elif age <= 12:
        if temps < 8:
            return "Excellent", "Tester avec obstacles supplémentaires"
        elif temps < 10:
            return "Bon", "Maintenir le rythme et affiner le contrôle"
        else:
            return "À améliorer", "Répéter les circuits courts sous pression"
    else:
        if temps < 7.5:
            return "Excellent", "Évaluer en condition de match"
        elif temps < 9.5:
            return "Bon", "Augmenter l’intensité avec contraintes"
        else:
            return "À améliorer", "Travailler en séquences courtes avec repos actif"

# 🔍 FONCTION IA – PASSE
def evaluer_passe(age, precision, pression):
    if precision >= 80:
        if pression == 12:
            return "Excellent", "Intégrer des passes en mouvement avec opposition"
        elif pression == 6:
            return "Très bon", "Simuler des passes sous pression dans espace réduit"
        else:
            return "Bon", "Travailler la vision et la vitesse d’exécution"
    elif precision >= 50:
        return "Moyen", "Augmenter la répétition avec variation de cible"
    else:
        return "À améliorer", "Corriger la posture et le geste de passe"

# 🔘 FORMULAIRE GÉNÉRAL
st.header(f"🧪 Test : {test_selection}")
nom = st.text_input("Nom du joueur", key=f"nom_{test_selection}")
age = st.number_input("Âge", min_value=8, max_value=18, step=1, key=f"age_{test_selection}")

# 🛣️ CONDUITE
if test_selection == "Conduite":
    temps_total = st.number_input("Temps total (en secondes)", min_value=0.0, step=0.01, key="temps_conduite")
    if st.button("➕ Ajouter ce test", key="add_conduite"):
        if nom and temps_total > 0:
            note, plan = evaluer_conduite(age, temps_total)
            ajouter_resultat("Conduite", {
                "Nom": nom,
                "Âge": age,
                "Temps (s)": temps_total,
                "Note": note,
                "Plan d'action": plan
            })

# 🎯 PASSE
if test_selection == "Passe":
    pied = st.selectbox("Pied utilisé", ["Droit", "Gauche"], key="pied_passe")
    pression = st.selectbox("Pression", ["Sans pression (12s)", "Pression moyenne (6s)", "Haute pression (3s)"], key="pression_passe")
    pression_val = {"Sans pression (12s)": 12, "Pression moyenne (6s)": 6, "Haute pression (3s)": 3}[pression]
    cibles_total = 6
    cibles_reussies = st.number_input("Cibles touchées (sur 6)", min_value=0, max_value=6, step=1, key="cibles_passe")
    
    if st.button("➕ Ajouter ce test", key="add_passe"):
        if nom:
            precision = (cibles_reussies / cibles_total) * 100
            note, plan = evaluer_passe(age, precision, pression_val)
            ajouter_resultat("Passe", {
                "Nom": nom,
                "Âge": age,
                "Pied": pied,
                "Pression": pression,
                "Précision (%)": round(precision, 1),
                "Note": note,
                "Plan d'action": plan
            })

# 📊 RÉSULTATS
if st.session_state["tests"][test_selection]:
    st.markdown("### 📊 Résultats")
    df = pd.DataFrame(st.session_state["tests"][test_selection])
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")_


