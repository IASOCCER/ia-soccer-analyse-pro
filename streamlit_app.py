import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.title("⚽ IA Soccer – Analyse Technique")

st.header("🛣️ Conduite de Balle – Circuit en L")

# Initialisation de la mémoire
if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

# Informations de base
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)
temps_total = st.number_input("Temps total (en secondes)", min_value=0.0, step=0.01)

# Fonction d'évaluation automatique
def evaluer_conduite(age, temps):
    # Références simples par âge (exemples)
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

# Ajouter le test
if st.button("➕ Ajouter ce test"):
    if nom and temps_total > 0:
        note, plan = evaluer_conduite(age, temps_total)
        st.session_state["conduite_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Temps (s)": temps_total,
            "Note": note,
            "Plan d'action": plan
        })
    else:
        st.warning("Veuillez entrer un nom et un temps valide.")

# Afficher les résultats
if st.session_state["conduite_tests"]:
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.markdown("### 📊 Résultats")
    st.dataframe(df, use_container_width=True)

    # Télécharger les résultats
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Télécharger les résultats (.csv)", csv, "conduite_balle.csv", "text/csv")


