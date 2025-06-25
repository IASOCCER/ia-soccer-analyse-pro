import streamlit as st
import openai
import pandas as pd

st.set_page_config(page_title="IA Soccer – Analyse du Remate", layout="wide")
st.title("🎯 IA Soccer – Analyse du Remate")

openai.api_key = st.secrets["openai"]["api_key"]

if "tir_tests" not in st.session_state:
    st.session_state["tir_tests"] = []

st.markdown("### 🧑‍🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

# Pied Droit
st.markdown("### 🦵 Pied Droit – 10 tirs")
acertos_d = 0
vitesses_d = []

for i in range(10):
    col1, col2 = st.columns([1, 2])
    with col1:
        touche = st.checkbox(f"🎯 Cible touchée (D{i+1})", key=f"droit_hit_{i}")
        if touche:
            acertos_d += 1
    with col2:
        vitesse = st.number_input(f"Vitesse du tir D{i+1} (km/h)", min_value=0.0, max_value=150.0, step=0.1, key=f"droit_speed_{i}")
        vitesses_d.append(vitesse)

# Pied Gauche
st.markdown("### 🦶 Pied Gauche – 10 tirs")
acertos_g = 0
vitesses_g = []

for i in range(10):
    col1, col2 = st.columns([1, 2])
    with col1:
        touche = st.checkbox(f"🎯 Cible touchée (G{i+1})", key=f"gauche_hit_{i}")
        if touche:
            acertos_g += 1
    with col2:
        vitesse = st.number_input(f"Vitesse du tir G{i+1} (km/h)", min_value=0.0, max_value=150.0, step=0.1, key=f"gauche_speed_{i}")
        vitesses_g.append(vitesse)

def generer_analyse_remate(nom, age, prec_d, prec_g, vit_d, vit_g):
    prompt = f"""
Tu es un expert en analyse technique de football pour jeunes joueurs.
Analyse la performance de {nom}, {age} ans, dans un exercice de remate avec 5 cibles.

- Précision pied droit : {prec_d}%
- Précision pied gauche : {prec_g}%
- Vitesse moyenne pied droit : {vit_d} km/h
- Vitesse moyenne pied gauche : {vit_g} km/h

Compare aux moyennes suivantes des académies professionnelles :
- U10–U12 : précision 40-60%, vitesse 40-55 km/h
- U13–U15 : précision 50-70%, vitesse 55-70 km/h
- U16–U18 : précision 60-80%, vitesse 65-85 km/h

Génère une évaluation et un plan d'action avec 3 exercices personnalisés à travailler.
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=600
    )
    return response.choices[0].message.content.strip()

if st.button("✅ Ajouter ce test"):
    precision_d = round(acertos_d / 10 * 100, 1)
    precision_g = round(acertos_g / 10 * 100, 1)
    vitesse_d = round(sum(vitesses_d) / len(vitesses_d), 1)
    vitesse_g = round(sum(vitesses_g) / len(vitesses_g), 1)

    analyse = generer_analyse_remate(nom, age, precision_d, precision_g, vitesse_d, vitesse_g)

    resultat = {
        "Nom": nom,
        "Âge": age,
        "Précision Droit (%)": precision_d,
        "Précision Gauche (%)": precision_g,
        "Vitesse Moy. Droit (km/h)": vitesse_d,
        "Vitesse Moy. Gauche (km/h)": vitesse_g,
        "Analyse IA": analyse
    }

    st.session_state["tir_tests"].append(resultat)

# Affichage des résultats
if st.session_state["tir_tests"]:
    st.markdown("### 📋 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["tir_tests"])
    st.dataframe(df, use_container_width=True)

    st.markdown("### 📊 Analyse IA du dernier test :")
    st.write(st.session_state["tir_tests"][-1]["Analyse IA"])

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les résultats (.csv)",
        data=csv,
        file_name="analyse_remate_ia_soccer.csv",
        mime="text/csv"
    )


