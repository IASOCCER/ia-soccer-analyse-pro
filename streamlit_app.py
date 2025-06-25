import streamlit as st
from datetime import datetime
from openai import OpenAI

# Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Analyse de la Masse Musculaire – IA Soccer", layout="wide")
st.title("💪 IA Soccer – Évaluation de la Masse Musculaire")

# Initialisation
if "muscle_tests" not in st.session_state:
    st.session_state["muscle_tests"] = []

st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### ⚖️ Données de composition corporelle")
poids = st.number_input("Poids total (kg)", min_value=10.0, step=0.1)
masse_musculaire = st.number_input("Masse musculaire (kg)", min_value=5.0, step=0.1)

# Références par âge
def get_reference_muscle(age):
    if age <= 10:
        return {"excellent": 20, "bon": 16}
    elif age <= 12:
        return {"excellent": 25, "bon": 20}
    elif age <= 14:
        return {"excellent": 30, "bon": 25}
    elif age <= 16:
        return {"excellent": 35, "bon": 30}
    else:
        return {"excellent": 40, "bon": 34}

# Évaluation simple
def evaluer_muscle(age, masse):
    ref = get_reference_muscle(age)
    note = 100
    if masse >= ref["excellent"]:
        niveau = "Excellent"
    elif masse >= ref["bon"]:
        note -= 15
        niveau = "Bon"
    else:
        note -= 30
        niveau = "À améliorer"
    return niveau, note, ref

# Analyse IA
def generer_analyse_muscle(nom, age, poids, masse, niveau):
    pourcentage = (masse / poids) * 100
    prompt = f"""
Le joueur {nom}, âgé de {age} ans, a été évalué avec une masse musculaire de {masse:.1f} kg sur un poids total de {poids:.1f} kg, soit environ {pourcentage:.1f}% de masse musculaire. Son niveau a été classé : {niveau}.

Fournis une analyse professionnelle de sa composition corporelle et un plan d'action personnalisé pour améliorer sa masse musculaire et sa condition physique. Inclure si pertinent des suggestions nutritionnelles et de renforcement musculaire.

Réponds en français de façon structurée, claire et adaptée à son âge.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un préparateur physique expert en jeunes athlètes de football."},
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
    niveau, note, ref = evaluer_muscle(age, masse_musculaire)
    analyse = generer_analyse_muscle(nom, age, poids, masse_musculaire, niveau)
    test = {
        "nom": nom,
        "âge": age,
        "poids": poids,
        "masse_musculaire": masse_musculaire,
        "niveau": niveau,
        "note": note,
        "réf": ref,
        "analyse": analyse,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.session_state["muscle_tests"].append(test)
    st.success("✅ Test ajouté avec succès.")

# Affichage
st.markdown("### 📊 Tests enregistrés")
for i, t in enumerate(st.session_state["muscle_tests"]):
    pourcent = (t['masse_musculaire'] / t['poids']) * 100
    st.write(f"**Test {i+1} – {t['date']}**")
    st.write(f"👤 {t['nom']} | Âge: {t['âge']}")
    st.write(f"⚖️ Masse musculaire: {t['masse_musculaire']} kg / {t['poids']} kg ({pourcent:.1f}%)")
    st.write(f"📈 Note: {t['note']} /100 – Niveau: **{t['niveau']}**")
    st.markdown(f"🧠 **Analyse IA** :\n\n{t['analyse']}")
    st.markdown("---")

if st.session_state["muscle_tests"]:
    if st.button("📄 Générer le rapport final"):
        st.markdown("✅ Rapport généré. (Exportation PDF et sauvegarde Google Drive à venir.)")









