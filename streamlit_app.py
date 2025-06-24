import streamlit as st
import pandas as pd
import openai

# Configuração da página
st.set_page_config(page_title="IA Soccer – Conduite de Balle avec IA", layout="wide")
st.title("🚀 IA Soccer – Analyse de Conduite de Balle (avec Intelligence Artificielle)")

# Inicializar memória
if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

# Nova forma de autenticar com OpenAI
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# Formulário do jogador
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🛣️ Détails du test de conduite de balle")
parcours = st.selectbox("Type de parcours", [
    "Parcours Zig-Zag (6 cônes, 15m au total)",
    "Parcours avec Changements de Direction (3 virages, 12m)"
])
temps = st.number_input("⏱️ Temps (en secondes)", min_value=0.0, step=0.1)

perte_controle = False
if parcours == "Parcours avec Changements de Direction (3 virages, 12m)":
    perte_controle = st.radio("❌ Perte de contrôle de la balle ?", ["Non", "Oui"]) == "Oui"

# Função para gerar análise com IA
def generer_plan_ia(nom, age, parcours, temps, perte_controle):
    prompt = f"""
Le joueur s'appelle {nom}, il a {age} ans.
Il a effectué le test suivant : {parcours}
Temps réalisé : {temps} secondes.
Perte de contrôle de la balle : {"Oui" if perte_controle else "Non"}

Agis comme un entraîneur professionnel d'une académie de haut niveau. 
Génère un plan d'action technique personnalisé en français avec :
1. Un commentaire technique sur la performance
2. 2 exercices recommandés (précis)
3. Un plan de progression sur 7 jours
4. Conseils techniques adaptés à son âge
Réponds en 5 lignes maximum.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Erreur lors de l'appel à l'IA : {str(e)}"

# Botão para adicionar teste
if st.button("✅ Ajouter ce test avec analyse IA"):
    analyse = generer_plan_ia(nom, age, parcours, temps, perte_controle)

    st.session_state["conduite_tests"].append({
        "Nom": nom,
        "Âge": age,
        "Parcours": parcours,
        "Temps (s)": temps,
        "Perte de Contrôle": "Oui" if perte_controle else "Non",
        "Analyse IA": analyse
    })

    st.success("✅ Test ajouté avec succès. Voir analyse ci-dessous 👇")
    st.markdown(f"### 📊 Analyse IA pour {nom}:\n\n{analyse}")

# Exibir resultados
if st.session_state["conduite_tests"]:
    st.markdown("### 📋 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les résultats (.csv)",
        data=csv,
        file_name="analyse_conduite_ia_soccer.csv",
        mime="text/csv"
    )
