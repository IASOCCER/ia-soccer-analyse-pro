import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyse de Passe – IA Soccer", layout="wide")
st.title("🧠 IA Soccer – Analyse du Passe avec IA")

st.markdown("### 🎯 Exercice de Précision de Passe (6 cibles à 6 mètres)")

# Infos joueur
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)
pied = st.selectbox("Pied utilisé", ["Pied dominant", "Pied non-dominant"])
pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"])

# Résultats
st.markdown("#### Résultats de l'exercice")
nb_acertes = st.slider("Nombre de passes réussies sur 6", 0, 6, 4)
temps_reactions = []
st.markdown("Saisir les temps de réaction (en secondes) pour chaque passe réussie :")

for i in range(1, nb_acertes + 1):
    t = st.number_input(f"Temps pour la passe {i}", min_value=0.0, max_value=15.0, step=0.1, key=f"passe_{i}")
    temps_reactions.append(t)

# Rapport
if st.button("🧾 Générer le rapport"):
    precision = round((nb_acertes / 6) * 100, 1)
    temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if temps_reactions else 0.0

    st.success("✅ Rapport généré avec succès!")

    st.markdown(f"""
### 🔎 Résumé

- **Nom:** {nom}  
- **Âge:** {age}  
- **Pied utilisé:** {pied}  
- **Pression:** {pression}  
- **Passes réussies:** {nb_acertes}/6  
- **Précision:** {precision}%  
- **Temps moyen de réaction:** {temps_moyen} s
""")

    st.markdown("### 🧠 Analyse automatique")

    if precision >= 70:
        st.markdown("- ✅ **Précision élevée** – bon contrôle.")
    elif 50 <= precision < 70:
        st.markdown("- ⚠️ **Précision moyenne** – amélioration possible.")
    else:
        st.markdown("- ❌ **Faible précision** – travailler la régularité et la concentration.")

    if temps_moyen < 4:
        st.markdown("- ✅ **Réaction rapide** – excellente lecture du stimulus.")
    elif 4 <= temps_moyen <= 6:
        st.markdown("- ⚠️ **Réaction modérée** – à améliorer.")
    else:
        st.markdown("- ❌ **Réaction lente** – s'entraîner sous pression réelle.")

    if pied == "Pied non-dominant" and precision < 60:
        st.markdown("- 🦶 **Faiblesse du pied non-dominant** – intégrer des exercices spécifiques.")

    st.markdown("### 📌 Plan d'action recommandé")
    if precision < 60 or temps_moyen > 6:
        st.markdown("- 🔁 Répéter l'exercice avec pression progressive et feedback en temps réel.")
    else:
        st.markdown("- ✅ Maintenir le niveau et ajouter des contraintes de temps supplémentaires.")
