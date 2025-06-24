import streamlit as st
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

# --- Correção da chave privada ---
key_data = st.secrets["google_service_account"]
key_data["private_key"] = key_data["private_key"].replace("\\n", "\n")

# --- Inicializa credenciais ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(key_data, scope)
client = gspread.authorize(creds)

# --- Acesso à planilha e worksheet ---
sheet = client.open("IA Soccer Analyse Pro")  # nome da planilha no Google Sheets
worksheet = sheet.worksheet("Feuille 1")  # nome da aba

# --- Sessão do Streamlit ---
st.title("IA Soccer Analyse Pro - Teste de Passe")

# Inicializa lista de testes
if "tests" not in st.session_state:
    st.session_state["tests"] = []

# Formulário de entrada de dados
with st.form("formulaire_test"):
    nom = st.text_input("Nom du joueur")
    age = st.number_input("Âge", min_value=8, max_value=18, step=1)
    pied = st.selectbox("Pied utilisé", ["Droit", "Gauche"])
    pression = st.selectbox("Niveau de pression", ["Faible", "Moyenne", "Haute"])
    nb_reussies = st.number_input("Nombre de passes réussies (sur 6)", min_value=0, max_value=6)
    temps_moyen = st.number_input("Temps moyen pour chaque passe (s)", min_value=0.0, max_value=15.0, step=0.1)
    precision = round((nb_reussies / 6) * 100, 2)

    # Geração de plano de ação básico
    if precision >= 80:
        plan_action = "Excellent niveau de précision, continuer ainsi."
    elif precision >= 50:
        plan_action = "Bon niveau, travailler la régularité et la vitesse de réaction."
    else:
        plan_action = "Amélioration nécessaire en précision et concentration."

    submitted = st.form_submit_button("Ajouter ce test")

    if submitted:
        date = datetime.now().strftime("%Y-%m-%d")
        exercice = "Passe"

        test_data = {
            "Date": date,
            "Nom": nom,
            "Âge": age,
            "Exercice": exercice,
            "Pied": pied,
            "Niveau de pression": pression,
            "Précision (%)": precision,
            "Temps moyen (s)": temps_moyen,
            "Plan d'action": plan_action
        }

        st.session_state["tests"].append(test_data)

        # Salvar no Google Sheets
        worksheet.append_row([
            test_data["Date"],
            test_data["Nom"],
            test_data["Âge"],
            test_data["Exercice"],
            test_data["Pied"],
            test_data["Niveau de pression"],
            test_data["Précision (%)"],
            test_data["Temps moyen (s)"],
            test_data["Plan d'action"]
        ])

        st.success("✅ Teste adicionado com sucesso com plan d’action professionnel!")

# --- Exibição dos testes adicionados ---
if st.session_state["tests"]:
    st.markdown("### 📊 Résultats enregistrés (session en cours)")
    df = pd.DataFrame(st.session_state["tests"])
    st.dataframe(df, use_container_width=True)

