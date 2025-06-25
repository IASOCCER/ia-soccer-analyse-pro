import streamlit as st
import pandas as pd
import openai
import os

# Configuração da chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Analyse du Remate – IA Soccer", layout="wide")
st.title("⚽ IA Soccer – Analyse du Remate avec IA")

# Inicialização da memória
if "remate_tests" not in st.session_state:
    st.session_state["remate_tests"] = []

# Informações do jogador
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

# Registro dos chutes
st.markdown("### 🎯 Résultats des tirs")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pied droit")
    precision_d = st.slider("Précision (nombre de cibles atteintes sur 10)", 0, 10, 0)
    vitesses_d = [st.number_input(f"Vitesse tir {i+1} (km/h)", min_value=0.0, max_value=200.0, step=0.1, key=f"d{i}") for i in range(10)]
    vitesse_d = round(sum(vitesses_d) / 10, 2)

with col2:
    st.subheader("Pied gauche")
    precision_g = st.slider("Précision (nombre de cibles atteintes sur 10)", 0, 10, 0)
    vitesses_g = [st.number_input(f"Vitesse tir {i+1} (km/h)", min_value=0.0, max_value=200.0, step=0.1, key=f"g{i}") for i in range(10)]
    vitesse_g = round(sum(vitesses_g) / 10, 2)

# Botão para gerar o teste
if st.button("✅ Ajouter ce test"):
    analyse = ""

    if nom and age:
        analyse = generer_analyse_remate(nom, age, precision_d * 10, precision_g * 10, vitesse_d, vitesse_g)

        test_data = {
            "Nom": nom,
            "Âge": age,
            "Précision Droit (%)": precision_d * 10,
            "Précision Gauche (%)": precision_g * 10,
            "Vitesse Moy. Droit (km/h)": vitesse_d,
            "Vitesse Moy. Gauche (km/h)": vitesse_g,
            "Analyse IA": analyse
        }

        st.session_state["remate_tests"].append(test_data)
        st.success("✅ Test ajouté avec succès !")
    else:
        st.warning("⚠️ Veuillez remplir toutes les informations du joueur.")

# Exibição do resultado
if st.session_state["remate_tests"]:
    st.markdown("### 📊 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["remate_tests"])
    st.dataframe(df)

    dernier_test = st.session_state["remate_tests"][-1]
    st.markdown("### 🧠 Analyse IA")
    st.write(dernier_test["Analyse IA"])

# Função de geração da análise com IA
def generer_analyse_remate(nom, age, precision_d, precision_g, vitesse_d, vitesse_g):
    prompt = f"""
    Analyse la performance d’un joueur de football en fonction des données suivantes :

    - Nom : {nom}
    - Âge : {age} ans
    - Précision du pied droit : {precision_d} %
    - Précision du pied gauche : {precision_g} %
    - Vitesse moyenne du tir du pied droit : {vitesse_d} km/h
    - Vitesse moyenne du tir du pied gauche : {vitesse_g} km/h

    Détaille une analyse technique complète de ses performances au tir (remate), puis génère un plan d’action personnalisé avec 3 à 5 recommandations concrètes pour améliorer sa puissance, sa précision ou sa technique.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un entraîneur expert en analyse technique de football."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )
        return response.choices[0].message.content

    except openai.error.AuthenticationError:
        return "❌ Erreur d'authentification avec l'API OpenAI. Vérifie ta clé API dans Streamlit Cloud (secrets)."
    except Exception as e:
        return f"❌ Une erreur est survenue : {str(e)}"


