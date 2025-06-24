import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- Configurações iniciais ---
st.set_page_config(page_title="IA Soccer Analyse Pro", layout="centered")
st.title("📊 IA Soccer Analyse Pro – Teste de Passe")

# --- Conectar com o Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 👇 Corrigido para evitar erro com st.secrets
key_data = dict(st.secrets["gcp_service_account"])
key_data["private_key"] = key_data["private_key"].replace("\\n", "\n")

creds = ServiceAccountCredentials.from_json_keyfile_dict(key_data, scope)
client = gspread.authorize(creds)

# Abrir a planilha e aba específica
spreadsheet = client.open("IA Soccer – Données des tests")
worksheet = spreadsheet.worksheet("Test Passe")

# --- Formulário para o teste ---
st.markdown("### 📝 Ajouter un test de passe")

if "tests" not in st.session_state:
    st.session_state["tests"] = []

with st.form("formulaire_test"):
    nom = st.text_input("Nom du joueur")
    age = st.selectbox("Âge", list(range(8, 19)))
    pied = st.selectbox("Pied utilisé", ["Droit", "Gauche"])
    niveau = st.selectbox("Niveau de pression", ["Sans pression", "Pression moyenne", "Pression élevée"])
    nb_passes = st.number_input("Nombre de passes réussies (sur 6)", min_value=0, max_value=6, step=1)
    temps_moyen = st.number_input("Temps moyen entre le stimulus et la passe (en secondes)", min_value=0.0, step=0.1)
    plan_action = st.text_area("Plan d'action proposé")

    submit = st.form_submit_button("Ajouter ce test")

    if submit:
        precision = (nb_passes / 6) * 100
        date = datetime.now().strftime("%Y-%m-%d")
        exercice = "Passe"

        test_data = {
            "Date": date,
            "Nom": nom,
            "Âge": age,
            "Exercice": exercice,
            "Pied": pied,
            "Niveau de pression": niveau,
            "Précision (%)": round(precision, 2),
            "Temps moyen (s)": round(temps_moyen, 2),
            "Plan d'action": plan_action
        }

        st.session_state["tests"].append(test_data)

        # Salvar no Google Sheets
        worksheet.append_row([
            date,
            nom,
            age,
            exercice,
            pied,
            niveau,
            round(precision, 2),
            round(temps_moyen, 2),
            plan_action
        ])

        st.success("✅ Teste adicionado com sucesso com plan d’action professionnel!")

# --- Exibir os resultados da sessão ---
if st.session_state["tests"]:
    st.markdown("### 📊 Résultats enregistrés (session en cours)")
    df = pd.DataFrame(st.session_state["tests"])
    st.dataframe(df, use_container_width=True)

