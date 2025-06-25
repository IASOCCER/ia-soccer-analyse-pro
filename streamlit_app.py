import streamlit as st
import pandas as pd
from openai import OpenAI

st.write("Chave está visível?", "OPENAI_API_KEY" in st.secrets)

# Conexão segura com OpenAI (usando secrets do Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuração da página
st.set_page_config(page_title="IA Soccer – Analyse du Remate", layout="wide")
st.title("⚽ IA Soccer – Analyse du Remate Technique avec IA")

# Inicialização da sessão
if "tests_remate" not in st.session_state:
    st.session_state["tests_remate"] = []

# Informações do jogador
st.markdown("### 👤 Informations du Joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

# Dados do pé direito
st.markdown("### 🦵 Pied Droit")
precision_d = st.slider("🎯 Précision (sur 10 tirs)", 0, 10, 0, key="precision_d")
vitesses_d = [st.number_input(f"Vitesse Tir {i+1} (km/h)", 0.0, 200.0, step=0.1, key=f"v_d{i}") for i in range(10)]
vitesse_d_moy = round(sum(vitesses_d) / 10, 2)

# Dados do pé esquerdo
st.markdown("### 🦵 Pied Gauche")
precision_g = st.slider("🎯 Précision (sur 10 tirs)", 0, 10, 0, key="precision_g")
vitesses_g = [st.number_input(f"Vitesse Tir {i+1} (km/h)", 0.0, 200.0, step=0.1, key=f"v_g{i}") for i in range(10)]
vitesse_g_moy = round(sum(vitesses_g) / 10, 2)

# Base de referência
base_ref = {
    10: {"precision": 50, "vitesse": 45},
    11: {"precision": 55, "vitesse": 50},
    12: {"precision": 60, "vitesse": 55},
    13: {"precision": 65, "vitesse": 60},
    14: {"precision": 70, "vitesse": 65},
    15: {"precision": 75, "vitesse": 70},
    16: {"precision": 80, "vitesse": 75},
    17: {"precision": 85, "vitesse": 80},
    18: {"precision": 90, "vitesse": 85},
}

# Função para gerar a análise com IA
def generer_analyse_remate(nom, age, precision_d, precision_g, vitesse_d, vitesse_g):
    ref = base_ref.get(age, {"precision": 65, "vitesse": 60})
    precision_moy = (precision_d + precision_g) / 2
    vitesse_moy = (vitesse_d + vitesse_g) / 2
    ecart_precision = round(precision_moy - ref["precision"], 1)
    ecart_vitesse = round(vitesse_moy - ref["vitesse"], 1)

    comparaison = f"""
### 📈 Comparaison avec les standards pour {age} ans :
- Précision moyenne : {precision_moy:.1f}% (écart de {ecart_precision:+.1f}%)
- Vitesse moyenne : {vitesse_moy:.1f} km/h (écart de {ecart_vitesse:+.1f} km/h)
"""

    prompt = f"""
{comparaison}

Fais une analyse technique complète des tirs de ce joueur ({nom}, {age} ans).
Puis, propose un plan d'action personnalisé avec 3 à 5 conseils concrets pour améliorer sa puissance, sa précision et sa posture.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un entraîneur professionnel spécialisé en analyse technique du football."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )
        return comparaison + "\n" + response.choices[0].message.content
    except Exception as e:
        if "authentication" in str(e).lower():
            return "❌ Erreur d'authentification – vérifie ta clé API OpenAI."
        return f"❌ Une erreur est survenue : {e}"

# Botão de adicionar o teste
if st.button("✅ Ajouter ce test"):
    if nom and age:
        analyse = generer_analyse_remate(
            nom, age,
            precision_d * 10, precision_g * 10,
            vitesse_d_moy, vitesse_g_moy
        )

        test = {
            "Nom": nom,
            "Âge": age,
            "Précision Droit (%)": precision_d * 10,
            "Précision Gauche (%)": precision_g * 10,
            "Vitesse Moy. Droit (km/h)": vitesse_d_moy,
            "Vitesse Moy. Gauche (km/h)": vitesse_g_moy,
            "Analyse IA": analyse
        }

        st.session_state["tests_remate"].append(test)
        st.success("✅ Test enregistré avec succès !")
    else:
        st.warning("⚠️ Veuillez remplir toutes les informations du joueur.")

# Exibição dos resultados
if st.session_state["tests_remate"]:
    st.markdown("### 📊 Résultat du dernier test")
    dernier = st.session_state["tests_remate"][-1]
    st.dataframe(pd.DataFrame([dernier]))

    st.markdown("### 🧠 Analyse IA")
    st.markdown(dernier["Analyse IA"])




