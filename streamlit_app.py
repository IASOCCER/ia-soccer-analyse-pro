import streamlit as st
from datetime import datetime
from openai import OpenAI

# Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Sprint – IA Soccer", layout="wide")
st.title("🏃‍♂️ IA Soccer – Analyse Professionnelle du Sprint")

# Initialisation
if "sprint_tests" not in st.session_state:
    st.session_state["sprint_tests"] = []

st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🛣️ Type de test de sprint")
type_sprint = st.selectbox("Choisissez la distance du sprint", ["Sprint 10m", "Sprint 20m"])
temps = st.number_input("Temps réalisé (en secondes)", min_value=0.0, step=0.01)

# Références comparatives
def get_reference(age, type_sprint):
    ref = {}
    if type_sprint == "Sprint 10m":
        if age <= 10: ref = {"excellent": 2.2, "bon": 2.7}
        elif age <= 12: ref = {"excellent": 2.0, "bon": 2.5}
        elif age <= 14: ref = {"excellent": 1.9, "bon": 2.4}
        elif age <= 16: ref = {"excellent": 1.8, "bon": 2.3}
        else: ref = {"excellent": 1.7, "bon": 2.2}
    else:
        if age <= 10: ref = {"excellent": 4.2, "bon": 4.8}
        elif age <= 12: ref = {"excellent": 4.0, "bon": 4.6}
        elif age <= 14: ref = {"excellent": 3.8, "bon": 4.4}
        elif age <= 16: ref = {"excellent": 3.6, "bon": 4.2}
        else: ref = {"excellent": 3.4, "bon": 4.0}
    return ref

# Analyse automatique + note
def evaluer_sprint(age, type_sprint, temps):
    ref = get_reference(age, type_sprint)
    note = 100
    if temps <= ref["excellent"]:
        niveau = "Excellent"
    elif temps <= ref["bon"]:
        note -= 15
        niveau = "Bon"
    else:
        note -= 30
        niveau = "À améliorer"
    return niveau, note, ref

# Analyse IA
def generer_analyse_sprint(age, type_sprint, temps, niveau):
    prompt = f"""
Un joueur de {age} ans a effectué un test de sprint de type '{type_sprint}' et a réalisé un temps de {temps:.2f} secondes. 
Niveau évalué : {niveau}.

1. Fournis une évaluation professionnelle en français.
2. Donne une explication sur sa performance selon l'âge et la distance.
3. Propose un plan d'action clair et personnalisé pour améliorer son sprint.

Sois concis, structuré et professionnel.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un coach de football spécialisé en performance physique."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur IA : {str(e)}"

# Ajouter le test
if st.button("➕ Ajouter ce test"):
    niveau, note, ref = evaluer_sprint(age, type_sprint, temps)
    analyse = generer_analyse_sprint(age, type_sprint, temps, niveau)
    test = {
        "nom": nom,
        "âge": age,
        "type": type_sprint,
        "temps": temps,
        "niveau": niveau,
        "note": note,
        "réf": ref,
        "analyse": analyse,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.session_state["sprint_tests"].append(test)
    st.success("✅ Test ajouté avec succès.")

# Affichage
st.markdown("### 📊 Tests enregistrés")
for i, t in enumerate(st.session_state["sprint_tests"]):
    st.write(f"**Test {i+1} – {t['date']}**")
    st.write(f"👤 {t['nom']} | Âge: {t['âge']} | Type: {t['type']}")
    st.write(f"⏱️ Temps: {t['temps']} s | Référence: Excellent ≤ {t['réf']['excellent']}s / Bon ≤ {t['réf']['bon']}s")
    st.write(f"📈 Note: {t['note']} /100 – Niveau: **{t['niveau']}**")
    st.markdown(f"🧠 **Analyse IA** :\n\n{t['analyse']}")
    st.markdown("---")

# Rapport final
if st.session_state["sprint_tests"]:
    if st.button("📄 Générer le rapport final"):
        st.markdown("✅ Rapport généré. (Exportation PDF et sauvegarde Drive disponibles bientôt)")








