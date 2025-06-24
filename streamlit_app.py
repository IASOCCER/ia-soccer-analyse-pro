import streamlit as st
import pandas as pd
from openai import OpenAI

# Autenticação correta da API:
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Analyse de Remate – IA Soccer", layout="wide")
st.title("🔥 IA Soccer – Analyse du Remate")

base_reference = {
    8: {"vitesse": 40, "precision": 30},
    9: {"vitesse": 45, "precision": 35},
    10: {"vitesse": 50, "precision": 40},
    11: {"vitesse": 55, "precision": 45},
    12: {"vitesse": 60, "precision": 50},
    13: {"vitesse": 65, "precision": 55},
    14: {"vitesse": 70, "precision": 60},
    15: {"vitesse": 75, "precision": 65},
    16: {"vitesse": 80, "precision": 70},
    17: {"vitesse": 85, "precision": 75},
    18: {"vitesse": 90, "precision": 80}
}

if "remate_tests" not in st.session_state:
    st.session_state["remate_tests"] = []

st.markdown("### 🧑‍🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🥅 Détails du test de remate")
distance = st.selectbox("Distance du tir (m)", [6, 8, 10])
nb_tirs = st.number_input("Nombre total de tirs", min_value=1, value=10)
nb_alvo = st.number_input("Nombre d'alvéoles touchées", min_value=0, max_value=nb_tirs)
vitesse = st.number_input("Vitesse moyenne du tir (km/h)", min_value=0)
pied = st.selectbox("Pied utilisé", ["Droit", "Gauche"])

if st.button("✅ Ajouter ce test"):
    precision = round((nb_alvo / nb_tirs) * 100, 1) if nb_tirs else 0
    ref = base_reference.get(age, {"vitesse": 60, "precision": 50})

    niveau = "Insuffisant"
    if precision >= ref["precision"] and vitesse >= ref["vitesse"]:
        niveau = "Excellent"
    elif precision >= ref["precision"] - 10 and vitesse >= ref["vitesse"] - 10:
        niveau = "Bon"
    elif precision >= ref["precision"] - 20 and vitesse >= ref["vitesse"] - 20:
        niveau = "Moyen"

    # Função atualizada da IA:
    def generer_analyse_ia(nom, age, distance, nb_tirs, nb_alvo, vitesse, pied, niveau):
        prompt = f"""
Tu es un entraîneur professionnel. Analyse ce test de remate :
Nom : {nom}, Âge : {age} ans, Distance : {distance} m, Tirs : {nb_tirs}, Alvéoles touchées : {nb_alvo}, Vitesse : {vitesse} km/h, Pied : {pied}.
Niveau : {niveau}.
Compare avec les standards des grandes académies (PSG, Real Madrid, Benfica). Analyse précision et puissance, puis propose un plan d’action en 3 exercices et progression sur 7 jours.
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    analyse = generer_analyse_ia(nom, age, distance, nb_tirs, nb_alvo, vitesse, pied, niveau)

    test = {
        "Nom": nom,
        "Âge": age,
        "Distance (m)": distance,
        "Tirs": nb_tirs,
        "Alvéoles touchées": nb_alvo,
        "Précision (%)": precision,
        "Vitesse (km/h)": vitesse,
        "Pied": pied,
        "Niveau": niveau,
        "Analyse IA": analyse
    }
    st.session_state["remate_tests"].append(test)
    st.success("✅ Test ajouté avec succès !")

if st.session_state["remate_tests"]:
    st.markdown("### 📊 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["remate_tests"])
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les résultats (.csv)",
        data=csv,
        file_name="analyse_remate_ia_soccer.csv",
        mime="text/csv"
    )

