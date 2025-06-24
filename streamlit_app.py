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
        st.markdown("""
#### 🟥 Niveau Prioritaire – Amélioration urgente

**🎯 Objectif technique :** Améliorer la précision du passe sous pression et la prise de décision rapide.  
**🧪 Exercices recommandés :**
- Passe courte avec cible visuelle (Blazepod ou plots)
- Enchaînement contrôle-passe en triangle avec changement de direction
- Jeu à 1 touche dans un espace réduit
- Exercice de prise d'information + passe rapide (scanning + exécution)

**📆 Fréquence :** 3 fois par semaine pendant 4 semaines  
**📌 Objectif de progrès :** Atteindre au moins 70% de précision en pression moyenne
        """)
    elif 60 <= precision < 70 or 4 <= temps_moyen <= 6:
        st.markdown("""
#### 🟨 Niveau Modéré – Consolider les acquis

**🎯 Objectif technique :** Stabiliser la régularité du passe sous pression modérée.  
**🧪 Exercices recommandés :**
- Passe à 2 touches avec changement d'appui
- Variation de surfaces de passe (intérieur, extérieur)
- Travail de passe après course courte (effort + précision)

**📆 Fréquence :** 2 fois par semaine pendant 3 semaines  
**📌 Objectif :** Maintenir au-dessus de 70% et progresser en situation de pression élevée
        """)
    else:
        st.markdown("""
#### 🟩 Niveau Avancé – Maintien et transfert en situation réelle

**🎯 Objectif technique :** Intégrer la qualité de passe dans le jeu réel.  
**🧪 Exercices recommandés :**
- Jeu réduit avec contrainte de 1 touche
- Passe en 3e homme avec changement de tempo
- Analyse vidéo de timing de passe et prise d'initiative

**📆 Fréquence :** 1 session spécifique par semaine  
**📌 Objectif :** Transfert vers les matchs et prise de décision rapide en zone dense
        """)

