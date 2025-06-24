import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Autenticação com Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
spreadsheet = client.open("IA Soccer - Données Techniques")
worksheet = spreadsheet.worksheet("Passe")

# --- Configuração da página ---
st.set_page_config(page_title="Analyse de Passe – IA Soccer", layout="wide")
st.title("⚽ IA Soccer – Analyse du Passe avec IA")

# --- Inicialização da memória ---
if "tests" not in st.session_state:
    st.session_state["tests"] = []

# --- Informações do jogador ---
st.markdown("### 🧍 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

# --- Detalhes do teste ---
st.markdown("### 🎯 Détails du test")
pied = st.selectbox("Pied utilisé", ["Pied gauche", "Pied droit"])
pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"])
nb_acertes = st.selectbox("Nombre de passes réussies sur 6", [0, 1, 2, 3, 4, 5, 6])

# --- Captura dos tempos de reação ---
temps_reactions = []
if nb_acertes > 0:
    st.markdown("Saisir les temps de réaction (en secondes) pour chaque passe réussie :")
    for i in range(1, nb_acertes + 1):
        t = st.number_input(f"Temps pour la passe {i}", min_value=0.0, max_value=15.0, step=0.1, key=f"passe_{i}")
        temps_reactions.append(t)

# --- Botão para adicionar o teste ---
if st.button("+ Ajouter ce test"):
    if nom and age:
        precision = round((nb_acertes / 6) * 100, 1)
        temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if nb_acertes > 0 else 0.0

        # --- Geração do plano de ação profissional ---
        if precision < 60 or temps_moyen > 6:
            plan = """🟥 Niveau Prioritaire – Amélioration urgente

**Objectif :** Améliorer la précision du passe sous pression et la prise de décision rapide.  
**Exercices recommandés :**
- Passe courte avec cible visuelle (Blazepod ou plots)
- Enchaînement contrôle-passe en triangle
- Jeu à 1 touche dans un espace réduit
- Scanning visuel avant l'exécution

**Fréquence :** 3 fois par semaine pendant 4 semaines  
**Cible :** Atteindre 70% de précision en pression moyenne"""
        elif 60 <= precision < 70 or 4 <= temps_moyen <= 6:
            plan = """🟨 Niveau Modéré – Consolider les acquis

**Objectif :** Stabiliser la régularité du passe sous pression modérée.  
**Exercices recommandés :**
- Passe à 2 touches avec changement d'appui
- Variation de surfaces de passe
- Travail après course courte (effort + précision)

**Fréquence :** 2 fois par semaine pendant 3 semaines  
**Cible :** Maintenir au-dessus de 70% en situation réelle"""
        else:
            plan = """🟩 Niveau Avancé – Maintien et transfert

**Objectif :** Intégrer la qualité de passe dans le jeu réel.  
**Exercices recommandés :**
- Jeu réduit avec 1 touche
- Passe en 3e homme
- Analyse vidéo de prise d'information

**Fréquence :** 1 session spécifique/semaine  
**Cible :** Transfert vers les matchs"""

        # Dados do teste
        test_data = {
            "Nom": nom,
            "Âge": age,
            "Pied": pied,
            "Niveau de pression": pression,
            "Nb passes réussies": nb_acertes,
            "Temps moyen (s)": temps_moyen,
            "Précision (%)": precision,
            "Plan d'action": plan
        }

        # Salvar localmente na sessão
        st.session_state["tests"].append(test_data)

        # Salvar no Google Sheets
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
        exercice = "Passe"

        worksheet.append_row([
            date,
            test_data["Nom"],
            test_data["Âge"],
            exercice,
            test_data["Pied"],
            test_data["Niveau de pression"],
            test_data["Précision (%)"],
            test_data["Temps moyen (s)"],
            test_data["Plan d'action"]
        ])

        st.success("✅ Teste adicionado com sucesso com plan d’action professionnel!")
