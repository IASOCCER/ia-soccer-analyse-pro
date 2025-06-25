import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Agilité Réactive – IA Soccer", layout="wide")
st.title("⚡ IA Soccer – Test d'Agilité Réactive (BlazePod)")

if "agility_tests" not in st.session_state:
    st.session_state["agility_tests"] = []

st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🧪 Paramètres du test")
pression = st.selectbox("Niveau de pression", [
    "🟢 Faible (4 sec entre les pods)",
    "🟠 Moyenne (2.5 sec entre les pods)",
    "🔴 Haute (1.5 sec entre les pods)"
])
temps_moyen = st.number_input("Temps moyen de réaction (en secondes)", min_value=0.0, step=0.1)
taps_reussis = st.number_input("Nombre de pods tapés avec succès", min_value=0, max_value=30, step=1)

def analyser_agilite(age, pression, taps, temps):
    seuils = {
        "🟢 Faible (4 sec entre les pods)": 3.2,
        "🟠 Moyenne (2.5 sec entre les pods)": 2.6,
        "🔴 Haute (1.5 sec entre les pods)": 2.2
    }
    seuil = seuils.get(pression, 3.0)
    
    if temps <= seuil:
        niveau = "Excellent"
        conseil = "Continuez à travailler sur la précision et la régularité sous pression."
    elif temps <= seuil + 0.5:
        niveau = "Bon"
        conseil = "Améliorez votre vitesse de réaction avec des exercices de changement de direction rapide."
    else:
        niveau = "À améliorer"
        conseil = "Travaillez votre explosivité et votre lecture des signaux visuels."

    return niveau, conseil

if st.button("➕ Ajouter ce test"):
    niveau, conseil = analyser_agilite(age, pression, taps_reussis, temps_moyen)
    test = {
        "nom": nom,
        "âge": age,
        "pression": pression,
        "taps": taps_reussis,
        "temps": temps_moyen,
        "niveau": niveau,
        "conseil": conseil,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.session_state["agility_tests"].append(test)
    st.success("✅ Test ajouté avec succès.")

st.markdown("### 📊 Tests enregistrés")
if st.session_state["agility_tests"]:
    for i, t in enumerate(st.session_state["agility_tests"]):
        st.write(f"**Test {i+1} – {t['date']}**")
        st.write(f"Nom: {t['nom']} | Âge: {t['âge']}")
        st.write(f"Pression: {t['pression']} | Taps réussis: {t['taps']} | Temps moyen: {t['temps']}s")
        st.write(f"🔎 **Niveau**: {t['niveau']} — 💡 **Plan d'action**: {t['conseil']}")
        st.markdown("---")
else:
    st.info("Aucun test enregistré pour l'instant.")

if st.session_state["agility_tests"]:
    if st.button("📄 Générer le rapport final"):
        st.markdown("✅ **Rapport généré.** (Export PDF et IA avancée à venir)")





