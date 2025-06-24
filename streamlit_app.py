import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analyse de Passe – IA Soccer", layout="wide")
st.title("🧠 IA Soccer – Analyse du Passe avec IA")

# Initialisation de la mémoire
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

        st.session_state["tests"].append({
            "Nom": nom,
            "Âge": age,
            "Pied": pied,
            "Pression": pression,
            "Précision (%)": precision,
            "Temps moyen (s)": temps_moyen
        })
        st.success("✅ Test ajouté avec succès!")
    else:
        st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

# Afficher les tests ajoutés
if st.session_state["tests"]:
    st.markdown("### 📊 Tests enregistrés")
    df = pd.DataFrame(st.session_state["tests"])
    st.dataframe(df, use_container_width=True)

    if st.button("📄 Générer le rapport final"):
        st.markdown(f"### 📌 Rapport final pour {nom}, {age} ans")

        for pied_type in ["Pied gauche", "Pied droit"]:
            sous_df = df[df["Pied"] == pied_type]
            if not sous_df.empty:
                st.markdown(f"#### 🦶 {pied_type}")
                st.dataframe(sous_df[["Pression", "Précision (%)", "Temps moyen (s)"]])

                precision_moy = sous_df["Précision (%)"].mean()
                temps_moy = sous_df["Temps moyen (s)"].mean()

                st.markdown(f"- **Précision moyenne :** {precision_moy:.1f}%")
                st.markdown(f"- **Temps moyen de réaction :** {temps_moy:.2f} s")

                # 🔍 Analyse
                st.markdown("### 🧠 Analyse automatique")
                if precision_moy >= 70:
                    st.markdown("- ✅ **Précision élevée** – bon contrôle.")
                elif 50 <= precision_moy < 70:
                    st.markdown("- ⚠️ **Précision moyenne** – amélioration possible.")
                else:
                    st.markdown("- ❌ **Faible précision** – travailler la régularité et la concentration.")

                if temps_moy < 4:
                    st.markdown("- ✅ **Réaction rapide** – excellente lecture du stimulus.")
                elif 4 <= temps_moy <= 6:
                    st.markdown("- ⚠️ **Réaction modérée** – à améliorer.")
                else:
                    st.markdown("- ❌ **Réaction lente** – s'entraîner sous pression réelle.")

                st.markdown("### 🎯 Plan d'action recommandé")

                if precision_moy < 60 or temps_moy > 6:
                    st.markdown("""
#### 🟥 Niveau Prioritaire – Amélioration urgente

**Objectif :** Améliorer la précision du passe sous pression et la prise de décision rapide.  
**Exercices :**
- Passe courte avec cible visuelle (Blazepod ou plots)
- Enchaînement contrôle-passe en triangle
- Jeu à 1 touche dans un espace réduit
- Scanning visuel avant l'exécution

**Fréquence :** 3 fois par semaine pendant 4 semaines  
**Objectif :** Atteindre 70% de précision en pression moyenne
                    """)
                elif 60 <= precision_moy < 70 or 4 <= temps_moy <= 6:
                    st.markdown("""
#### 🟨 Niveau Modéré – Consolider les acquis

**Objectif :** Stabiliser la régularité du passe sous pression modérée.  
**Exercices :**
- Passe à 2 touches avec changement d'appui
- Variation de surfaces de passe
- Travail après course courte (effort + précision)

**Fréquence :** 2 fois par semaine pendant 3 semaines  
**Objectif :** Maintenir au-dessus de 70% en situation réelle
                    """)
                else:
                    st.markdown("""
#### 🟩 Niveau Avancé – Maintien et transfert

**Objectif :** Intégrer la qualité de passe dans le jeu réel.  
**Exercices :**
- Jeu réduit avec 1 touche
- Passe en 3e homme
- Analyse vidéo de prise d'information

**Fréquence :** 1 session spécifique/semaine  
**Objectif :** Transfert vers les matchs
                    """)



