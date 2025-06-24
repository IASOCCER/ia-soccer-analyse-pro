import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configurer l'accès à Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

# Charger la feuille de calcul
spreadsheet = client.open("IA Soccer - Données Techniques")
worksheet = spreadsheet.sheet1

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="centered")

st.title("⚽ IA Soccer Analyse Pro - Test de Passe")

nom_joueur = st.text_input("👤 Nom du joueur")
age_joueur = st.number_input("🎂 Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🦵 Pied utilisé")
pied = st.selectbox("Choisissez le pied", ["Pied droit", "Pied gauche"])

st.markdown("### ⏱️ Type de pression")
pression = st.selectbox("Niveau de pression", ["Sans pression (12s)", "Pression modérée (6s)", "Haute pression (3s)"])

st.markdown("### 🎯 Précision du passe")
passes_reussies = st.number_input("Nombre de passes réussies sur 6", min_value=0, max_value=6, step=1)
precision = (passes_reussies / 6) * 100

st.markdown("### ⏳ Temps moyen par passe")
temps_moyen = st.number_input("Temps moyen (en secondes)", min_value=0.0, format="%.2f")

if "tests" not in st.session_state:
    st.session_state.tests = []

if st.button("Ajouter ce test"):
    st.session_state.tests.append({
        "Nom": nom_joueur,
        "Âge": age_joueur,
        "Pied": pied,
        "Pression": pression,
        "Précision (%)": precision,
        "Temps moyen (s)": temps_moyen,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success("✅ Test ajouté avec succès.")

if st.button("Sauvegarder tous les tests"):
    for test in st.session_state.tests:
        worksheet.append_row([
            test["Nom"],
            test["Âge"],
            test["Pied"],
            test["Pression"],
            test["Précision (%)"],
            test["Temps moyen (s)"],
            test["Date"]
        ])
    st.success("✅ Données sauvegardées avec succès sur Google Sheets.")
    st.session_state.tests = []

# Résumé et plan d'action
if st.session_state.get("tests"):
    st.markdown("---")
    st.markdown("## 📊 Résumé de l'analyse")

    precisions = [t["Précision (%)"] for t in st.session_state.tests]
    temps = [t["Temps moyen (s)"] for t in st.session_state.tests]

    precision_moy = sum(precisions) / len(precisions)
    temps_moy = sum(temps) / len(temps)

    st.markdown(f"**Précision moyenne :** {precision_moy:.1f}%")
    st.markdown(f"**Temps moyen global :** {temps_moy:.2f} s")

    st.markdown("### 📌 Plan d'action recommandé")

    if precision_moy < 60 or temps_moy > 6:
        st.markdown("""
#### 🟥 Niveau Prioritaire – Amélioration urgente

**🎯 Objectif technique :** Améliorer la précision du passe sous pression et la prise de décision rapide.  
**🧪 Exercices recommandés :**
- Passe courte avec cible visuelle (Blazepod ou plots)
- Enchaînement contrôle-passe en triangle avec changement de direction
- Jeu à 1 touche dans un espace réduit
- Exercice de prise d'information + passe rapide (scanning + exécution)

**📆 Fréquence :** 3 fois par semaine pendant 4 semaines  
**📌 Objectif de progrès :** Atteindre au moins 70% de précision en pression moyenne
        """)
    elif 60 <= precision_moy < 70 or 4 <= temps_moy <= 6:
        st.markdown("""
#### 🟨 Niveau Modéré – Consolider les acquis

**🎯 Objectif technique :** Stabiliser la régularité du passe sous pression modérée.  
**🧪 Exercices recommandés :**
- Passe à 2 touches avec changement d'appui
- Variation de surfaces de passe (intérieur, extérieur)
- Travail de passe après course courte (effort + précision)

**📆 Fréquence :** 2 fois par semaine pendant 3 semaines  
**📌 Objectif :** Maintenir au-dessus de 70% et progresser en situation de pression élevée
        """)
    else:
        st.markdown("""
#### 🟩 Niveau Avancé – Maintien et transfert en situation réelle

**🎯 Objectif technique :** Intégrer la qualité de passe dans le jeu réel.  
**🧪 Exercices recommandés :**
- Jeu réduit avec contrainte de 1 touche
- Passe en 3e homme avec changement de tempo
- Analyse vidéo de timing de passe et prise d'initiative

**📆 Fréquence :** 1 session spécifique par semaine  
**📌 Objectif :** Transfert vers les matchs et prise de décision rapide en zone dense
        """)

**Objectif :** Transfert vers les matchs
                    """)


