import streamlit as st
import pandas as pd
import openai
import os
from fpdf import FPDF

st.set_page_config(page_title="IA Soccer – Analyse de Conduite de Balle", layout="wide")
st.title("⚽ IA Soccer – Analyse de la Conduite de Balle")

# Authentification API OpenAI
openai.api_key = st.secrets["api_key"]

# Mémoire de session
if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

# Fonction d'analyse IA
def generer_analyse_ia(nom, age, type_parcours, temps, perte_controle):
    prompt = f"""
Tu es un expert en analyse technique de football pour jeunes joueurs. Analyse la performance suivante en français :
- Nom : {nom}
- Âge : {age} ans
- Type de parcours : {type_parcours}
- Temps réalisé : {temps} secondes
- Perte de contrôle de la balle : {'Oui' if perte_controle else 'Non'}

Compare la performance aux standards des grandes académies (ex. PSG, Real Madrid, Benfica) pour ce type d'exercice et ce groupe d'âge.
Fournis :
1. Un commentaire technique clair et synthétique.
2. Deux exercices recommandés.
3. Un plan de progression sur 7 jours.
4. Un conseil adapté à l'âge du joueur.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert de la formation technique au football."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content

# Fonction d'évaluation du niveau

def evaluer_niveau(age, temps, perte_controle, type_parcours):
    references = {
        "Parcours Zig-Zag (6 cônes, 15m au total)": {
            8: 11.0, 9: 10.5, 10: 10.0, 11: 9.5, 12: 9.0, 13: 8.5, 14: 8.0, 15: 7.5, 16: 7.0, 17: 6.5, 18: 6.0
        },
        "Parcours avec Changements de Direction (3 virages, 12m)": {
            8: 12.0, 9: 11.5, 10: 11.0, 11: 10.5, 12: 10.0, 13: 9.5, 14: 9.0, 15: 8.5, 16: 8.0, 17: 7.5, 18: 7.0
        }
    }
    ref = references[type_parcours].get(age, 10.0)

    if perte_controle:
        return "Faible"
    elif temps <= ref * 0.85:
        return "Excellent"
    elif temps <= ref:
        return "Bon"
    elif temps <= ref * 1.15:
        return "Moyen"
    else:
        return "Faible"

# Formulaire de saisie
st.markdown("### 🧑‍🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

st.markdown("### 🚚 Détails du test de conduite de balle")
type_parcours = st.selectbox("Type de parcours", [
    "Parcours Zig-Zag (6 cônes, 15m au total)",
    "Parcours avec Changements de Direction (3 virages, 12m)"
])
temps = st.number_input("⏱️ Temps (en secondes)", min_value=1.0, step=0.1)
perte_controle = st.radio("❌ Perte de contrôle de la balle ?", ["Non", "Oui"]) == "Oui"

if st.button("➕ Ajouter ce test avec analyse IA"):
    niveau = evaluer_niveau(age, temps, perte_controle, type_parcours)
    analyse = generer_analyse_ia(nom, age, type_parcours, temps, perte_controle)

    nouveau_test = {
        "Nom": nom,
        "Âge": age,
        "Parcours": type_parcours,
        "Temps (s)": temps,
        "Perte de Contrôle": "Oui" if perte_controle else "Non",
        "Niveau": niveau,
        "Analyse IA": analyse
    }
    st.session_state.conduite_tests.append(nouveau_test)
    st.success(f"Test ajouté avec succès. Niveau évalué: {niveau}")

# Affichage du dernier test
if st.session_state.conduite_tests:
    dernier_test = st.session_state.conduite_tests[-1]
    st.markdown(f"### 📊 Analyse IA pour {dernier_test['Nom']}:")
    st.markdown(dernier_test["Analyse IA"])

# Export PDF
    def exporter_pdf(test):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Nom: {test['Nom']}\nÂge: {test['Âge']}\nParcours: {test['Parcours']}\nTemps: {test['Temps (s)']}s\nPerte de Contrôle: {test['Perte de Contrôle']}\nNiveau: {test['Niveau']}\n\nAnalyse IA:\n{test['Analyse IA']}")
        nom_fichier = f"rapport_{test['Nom']}.pdf"
        pdf.output(nom_fichier)
        return nom_fichier

    if st.button("🔖 Télécharger le rapport PDF"):
        nom_pdf = exporter_pdf(dernier_test)
        with open(nom_pdf, "rb") as f:
            st.download_button("🔖 Télécharger le fichier PDF", f, file_name=nom_pdf)

# Tableau de résultats
if st.session_state.conduite_tests:
    st.markdown("### 📊 Résultats enregistrés")
    df = pd.DataFrame(st.session_state.conduite_tests)
    st.dataframe(df, use_container_width=True)
    st.download_button("📂 Télécharger les résultats (.csv)", df.to_csv(index=False).encode("utf-8"), file_name="resultats_conduite.csv")
