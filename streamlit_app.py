import streamlit as st
from datetime import datetime
import openai

# Configuração da chave OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Analyse Professionnelle – Agilité Réactive", layout="wide")
st.title("🚀 IA Soccer – Analyse Professionnelle de l'Agilité Réactive")

# Inicialização
if "agility_pro_tests" not in st.session_state:
    st.session_state["agility_pro_tests"] = []

# Interface – dados do jogador
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🧪 Détails du test")
pression = st.selectbox("Niveau de pression", [
    "🟢 Faible (4 sec)",
    "🟠 Moyenne (2.5 sec)",
    "🔴 Haute (1.5 sec)"
])
temps_moyen = st.number_input("Temps moyen de réaction (en secondes)", min_value=0.0, step=0.1)
taps_reussis = st.number_input("Nombre de pods tapés avec succès (sur 30)", min_value=0, max_value=30, step=1)

# Função com IA – gerar análise e plano
def generer_analyse_ia(age, pression, taps, temps):
    prompt = f"""
Tu es un entraîneur de haut niveau en football spécialisé dans l'agilité réactive. Un joueur de {age} ans a effectué un test d'agilité réactive avec un niveau de pression '{pression}'. 
Il a réussi {taps} touches sur 30 pods, avec un temps moyen de réaction de {temps:.2f} secondes.

1. Donne une évaluation globale de son niveau (Excellent, Bon, À améliorer).
2. Donne une analyse détaillée en lien avec son âge et la pression.
3. Propose un plan d'action clair et personnalisé pour améliorer sa performance.

Réponds de façon professionnelle, concise et en français.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un coach expert dans l'analyse de performance des joueurs de football."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Erreur IA: {str(e)}"

# Adicionar o teste
if st.button("➕ Ajouter ce test"):
    analyse_ia = generer_analyse_ia(age, pression, taps_reussis, temps_moyen)
    test = {
        "nom": nom,
        "âge": age,
        "pression": pression,
        "taps": taps_reussis,
        "temps": temps_moyen,
        "analyse": analyse_ia,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    st.session_state["agility_pro_tests"].append(test)
    st.success("✅ Test ajouté avec succès.")

# Mostrar os testes
st.markdown("### 📊 Tests enregistrés")
for i, t in enumerate(st.session_state["agility_pro_tests"]):
    st.write(f"**Test {i+1} – {t['date']}**")
    st.write(f"👤 {t['nom']} | Âge: {t['âge']} | Pression: {t['pression']}")
    st.write(f"🎯 Taps réussis: {t['taps']} /30")
    st.write(f"⏱️ Temps moyen: {t['temps']} secondes")
    st.markdown(f"🧠 **Analyse IA**:\n\n{t['analyse']}")
    st.markdown("---")

# Gerar relatório (em breve exportação PDF)
if st.session_state["agility_pro_tests"]:
    if st.button("📄 Générer le rapport final"):
        st.markdown("✅ **Rapport généré. Exportation PDF et sauvegarde Google Drive disponibles bientôt.**")






