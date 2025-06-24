import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Analyse de Passe – IA Soccer", layout="wide")
st.title("🧠 IA Soccer – Analyse du Passe avec IA")

# Conexão com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abrir a planilha pelo ID
sheet = client.open_by_key("1dqnkAFAFjbBpGJa37NrDdNfm8NYNrfWdaF5NDBsCgwg").sheet1

# Inicialização da memória
if "tests" not in st.session_state:
    st.session_state["tests"] = []

st.markdown("### 🧑‍🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

st.markdown("### 🎯 Détails du test")
pied = st.selectbox("Pied utilisé", ["Pied gauche", "Pied droit"])
pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"])
nb_acertes = st.slider("Nombre de passes réussies sur 6", 0, 6, 3)

temps_reactions = []
if nb_acertes > 0:
    st.markdown("Saisir les temps de réaction (en secondes) pour chaque passe réussie :")
    for i in range(1, nb_acertes + 1):
        t = st.number_input(f"Temps pour la passe {i}", min_value=0.0, max_value=15.0, step=0.1, key=f"passe_{i}")
        temps_reactions.append(t)

if st.button("➕ Ajouter ce test"):
    if nom and age:
        precision = round((nb_acertes / 6) * 100, 1)
        if nb_acertes == 0:
            temps_moyen = 0.0
        else:
            temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2)

        # Adicionar ao estado
        novo_teste = {
            "Nom": nom,
            "Âge": age,
            "Pied": pied,
            "Pression": pression,
            "Précision (%)": precision,
            "Temps moyen (s)": temps_moyen
        }

        st.session_state["tests"].append(novo_teste)

        # Salvar na planilha Google
        sheet.append_row(list(novo_teste.values()))

        st.success("✅ Test ajouté avec succès et sauvegardé dans Google Sheets!")
    else:
        st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

# Mostrar os dados locais
if st.session_state["tests"]:
    st.markdown("### 📊 Tests enregistrés (session actuelle)")
    df = pd.DataFrame(st.session_state["tests"])
    st.dataframe(df, use_container_width=True)



