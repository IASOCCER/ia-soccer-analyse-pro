import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="IA Soccer – Conduite de Balle avec IA", layout="wide")
st.title("🚀 IA Soccer – Analyse de Conduite de Balle (avec Intelligence Artificielle)")

if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🛣️ Détails du test de conduite de balle")
parcours = st.selectbox("Type de parcours", [
    "Parcours Zig-Zag (6 cônes, 15m au total)",
    "Parcours avec Changements de Direction (3 virages, 12m)"
])
temps = st.number_input("⏱️ Temps (en secondes)", min_value=0.0, step=0.1)

perte_controle = False
if parcours == "Parcours avec Changements de Direction (3 virages, 12m)":
    perte_controle = st.radio("❌ Perte de contrôle de la balle ?", ["Non", "Oui"]) == "Oui"

def generer_plan_ia(nom, age, parcours, temps, perte_controle):
    prompt = f"""
Le joueur s'appelle {nom}, il a {age} ans.
Il a effectué le test suivant : {parcours}
Temps réalisé : {temps} secondes.
Perte de contrôle de la balle : {"Oui" if perte_controle else "Non"}

Critères de performance pour le test :
- 8 à 10 ans : Excellent < 8.5s, Bon < 10s, Régulier < 11.5s, Faible ≥ 11.5s
- 11 à 13 ans : Excellent < 7.5s, Bon < 9s, Régulier < 10.5s, Faible ≥ 10.5s
- 14 à 18 ans : Excellent < 6.5s, Bon < 8s, Régulier < 9.5s, Faible ≥ 9.5s

Agis comme un entraîneur professionnel. Analyse objectivement la performance en fonction de ces critères. Si la performance est très faible, sois critique et propose un plan de correction.
Inclue dans ta réponse :
1. Un commentaire technique (1 ligne)
2. 2 exercices recommandés
3. Un plan de progression sur 7 jours
4. Des conseils adaptés à son âge

Réponds en 5 lignes professionnelles maximum.
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
    analyse = generer_plan_ia(nom, age, parcours, temps, perte_controle)

    st.session_state["conduite_tests"].append({
        "Nom": nom,
        "Âge": age,
        "Parcours": parcours,
        "Temps (s)": temps,
        "Perte de Contrôle": "Oui" if perte_controle else "Non",
        "Analyse IA": analyse
    })

    st.success("✅ Test ajouté avec succès. Voir analyse ci-dessous 👇")
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
from fpdf import FPDF
import base64
import io

def exporter_pdf(joueur):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title(f"Analyse IA – {joueur['Nom']}")
    pdf.cell(200, 10, txt=f"IA Soccer – Rapport Technique", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Nom: {joueur['Nom']}", ln=True)
    pdf.cell(200, 10, txt=f"Âge: {joueur['Âge']} ans", ln=True)
    pdf.cell(200, 10, txt=f"Parcours: {joueur['Parcours']}", ln=True)
    pdf.cell(200, 10, txt=f"Temps (s): {joueur['Temps (s)']} secondes", ln=True)
    pdf.cell(200, 10, txt=f"Perte de Contrôle: {joueur['Perte de Contrôle']}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"📊 Analyse IA:\n{joueur['Analyse IA']}")
    
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    b64_pdf = base64.b64encode(pdf_output.read()).decode('utf-8')

    st.markdown(f"""
        <a href="data:application/octet-stream;base64,{b64_pdf}" download="analyse_{joueur['Nom']}.pdf">
            📄 Télécharger le rapport PDF pour {joueur['Nom']}
        </a>
    """, unsafe_allow_html=True)

# Botão de exportação para o último jogador analisado
if st.session_state["conduite_tests"]:
    dernier_test = st.session_state["conduite_tests"][-1]
    exporter_pdf(dernier_test)
