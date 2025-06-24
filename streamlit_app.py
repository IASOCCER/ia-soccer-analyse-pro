import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="IA Soccer – Conduite Pro", layout="wide")
st.title("🚀 IA Soccer – Analyse Technique avec Références Professionnelles")

if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

from fpdf import FPDF

def exporter_pdf(test):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_text_color(0, 0, 128)
    pdf.cell(200, 10, txt="IA Soccer – Rapport de Test Technique", ln=True, align="C")
    pdf.ln(10)

    pdf.set_text_color(0, 0, 0)
    for clé, valeur in test.items():
        pdf.cell(200, 10, txt=f"{clé} : {valeur}", ln=True)

    pdf_output = "rapport_test_joueur.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as f:
        st.download_button(
            label="📄 Télécharger le PDF",
            data=f,
            file_name=pdf_output,
            mime="application/pdf"
        )

# Referências para Zig-Zag (6 cônes, 15m)
zigzag_ref = {
    8: 11.5, 9: 11.0, 10: 10.5, 11: 10.0, 12: 9.6, 13: 9.2,
    14: 8.9, 15: 8.6, 16: 8.4, 17: 8.2, 18: 8.0
}

# Referências para Changement de Direction (3 virages, 12m)
change_ref = {
    8: {"moyen": 16, "excellent": 14, "faible": 20},
    9: {"moyen": 15, "excellent": 13, "faible": 19},
    10: {"moyen": 14, "excellent": 12, "faible": 18},
    11: {"moyen": 13, "excellent": 11, "faible": 17},
    12: {"moyen": 12, "excellent": 10, "faible": 16},
    13: {"moyen": 11, "excellent": 9, "faible": 15},
    14: {"moyen": 10.5, "excellent": 8.5, "faible": 14.5},
    15: {"moyen": 10, "excellent": 8, "faible": 14},
    16: {"moyen": 9.5, "excellent": 7.5, "faible": 13.5},
    17: {"moyen": 9, "excellent": 7, "faible": 13},
    18: {"moyen": 9, "excellent": 7, "faible": 13}
}

st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🛣️ Détails du test")
parcours = st.selectbox("Type de parcours", [
    "Parcours Zig-Zag (6 cônes, 15m au total)",
    "Parcours avec Changements de Direction (3 virages, 12m)"
])
temps = st.number_input("⏱️ Temps (en secondes)", min_value=0.0, step=0.1)
perte_controle = False
if parcours.startswith("Parcours avec Changements"):
    perte_controle = st.radio("❌ Perte de contrôle de la balle ?", ["Non", "Oui"]) == "Oui"

def analyser_niveau(age, temps, parcours):
    if parcours.startswith("Parcours Zig-Zag"):
        ref = zigzag_ref.get(age, 10.0)
        if temps <= ref - 1.0:
            return "Excellent"
        elif temps <= ref + 1.0:
            return "Bon"
        elif temps <= ref + 3.0:
            return "Régulier"
        else:
            return "Faible"
    else:
        ref = change_ref.get(age, {"moyen": 12, "excellent": 10, "faible": 16})
        if temps <= ref["excellent"]:
            return "Excellent"
        elif temps >= ref["faible"]:
            return "Faible"
        elif temps <= ref["moyen"]:
            return "Bon"
        else:
            return "Régulier"

def generer_plan_ia(nom, age, parcours, temps, perte_controle, niveau):
    prompt = f"""
Le joueur s'appelle {nom}, {age} ans.
Exercice : {parcours}
Temps : {temps} s — Niveau évalué : {niveau}
Perte de contrôle : {"Oui" if perte_controle else "Non"}

Agis comme un entraîneur de haut niveau.
Crée un plan d'action personnalisé selon le niveau, l'âge et le type de parcours.
Inclue :
- Un commentaire technique
- 2 exercices recommandés
- Plan sur 7 jours
- Conseils d'amélioration

Réponds en 5 lignes maximum.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur lors de l'appel à l'IA : {str(e)}"

if st.button("✅ Ajouter ce test avec analyse IA"):
    niveau = analyser_niveau(age, temps, parcours)
    analyse = generer_plan_ia(nom, age, parcours, temps, perte_controle, niveau)

    st.session_state["conduite_tests"].append({
        "Nom": nom,
        "Âge": age,
        "Parcours": parcours,
        "Temps (s)": temps,
        "Perte de Contrôle": "Oui" if perte_controle else "Non",
        "Niveau": niveau,
        "Analyse IA": analyse
    })

    st.success(f"✅ Test ajouté avec succès. Niveau évalué: {niveau}")
    st.markdown(f"### 📊 Analyse IA pour {nom}:\n\n{analyse}")

if st.session_state["conduite_tests"]:
    st.markdown("### 📋 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les résultats (.csv)",
        data=csv,
        file_name="analyse_conduite_ia_soccer.csv",
        mime="text/csv"
    )
 # PDF du dernier test
    dernier_test = st.session_state["conduite_tests"][-1]

    if st.button("📄 Exporter le dernier test en PDF"):
        exporter_pdf(dernier_test)
