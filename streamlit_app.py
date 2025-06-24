import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="IA Soccer – Analyse du Remate", layout="wide")
st.title("🧠 IA Soccer – Analyse du Remate avec IA")

# Chave da API
openai.api_key = st.secrets["api_key"]

# Inicializar memória
if "remate_tests" not in st.session_state:
    st.session_state["remate_tests"] = []

# Função IA
def generer_analyse_ia(nom, age, precision_d, vitesse_d, precision_g, vitesse_g):
    prompt = f"""
Tu es un entraîneur professionnel. Fais une analyse technique complète du joueur {nom}, {age} ans.

Il a effectué 10 tirs avec le pied droit :
- Précision : {precision_d}%
- Vitesse moyenne : {vitesse_d} km/h

Et 10 tirs avec le pied gauche :
- Précision : {precision_g}%
- Vitesse moyenne : {vitesse_g} km/h

Fais une analyse par pied, compare avec les standards d'académies professionnelles (FC Porto, PSG, Barça) pour son âge. Termine par un plan d'action avec exercices personnalisés.
"""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=800
    )
    return response.choices[0].message.content

# Interface
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

st.markdown("### 🦵 Pied Droit – 10 tirs")
col_d = st.columns(10)
acertos_d = 0
vitesses_d = []

for i in range(10):
    with col_d[i]:
        if st.checkbox(f"🎯 D{i+1}", key=f"r_d{i}"):
            acertos_d += 1
        vitesse = st.number_input(f"V{i+1}", min_value=0.0, max_value=150.0, step=0.1, key=f"v_d{i}")
        vitesses_d.append(vitesse)

st.markdown("### 🦶 Pied Gauche – 10 tirs")
col_g = st.columns(10)
acertos_g = 0
vitesses_g = []

for i in range(10):
    with col_g[i]:
        if st.checkbox(f"🎯 G{i+1}", key=f"r_g{i}"):
            acertos_g += 1
        vitesse = st.number_input(f"V{i+1}", min_value=0.0, max_value=150.0, step=0.1, key=f"v_g{i}")
        vitesses_g.append(vitesse)

# Cálculos
if st.button("✅ Ajouter ce test"):
    precision_d = round(acertos_d / 10 * 100, 1)
    precision_g = round(acertos_g / 10 * 100, 1)
    vitesse_d = round(sum(vitesses_d) / len(vitesses_d), 1)
    vitesse_g = round(sum(vitesses_g) / len(vitesses_g), 1)

    analyse = generer_analyse_ia(nom, age, precision_d, vitesse_d, precision_g, vitesse_g)

    nouveau_test = {
        "Nom": nom,
        "Âge": age,
        "Précision Droit (%)": precision_d,
        "Vitesse Moy. Droit (km/h)": vitesse_d,
        "Précision Gauche (%)": precision_g,
        "Vitesse Moy. Gauche (km/h)": vitesse_g,
        "Analyse IA": analyse
    }

    st.session_state["remate_tests"].append(nouveau_test)
    st.success("✅ Test ajouté avec succès !")

# Mostrar resultados
if st.session_state["remate_tests"]:
    st.markdown("### 📋 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["remate_tests"])
    st.dataframe(df, use_container_width=True)

    st.markdown(f"### 📊 Analyse IA pour {df.iloc[-1]['Nom']}:")
    st.markdown(df.iloc[-1]["Analyse IA"])


