import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.title("⚽ IA Soccer – Analyse de la Conduite de Balle")

# Initialisation de la mémoire
if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

st.markdown("### 🧑‍\u🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

st.markdown("### 🛣️ Détails du test de conduite de balle")
parcours = st.selectbox("Type de parcours", [
    "Parcours Zig-Zag (6 plots en ligne, 2,5m entre chaque)",
    "Parcours Courbe (3 courbes autour de 3 plots écartés de 4m)"
])
temps_total = st.number_input("Temps total pour compléter le parcours (en secondes)", min_value=1.0, max_value=30.0, step=0.1)

if st.button("➕ Ajouter ce test de conduite"):
    if nom and age:
        st.session_state["conduite_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Parcours": parcours,
            "Temps (s)": temps_total
        })
        st.success("✅ Test ajouté avec succès!")
    else:
        st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

# Affichage des résultats
if st.session_state["conduite_tests"]:
    st.markdown("### 📊 Tests enregistrés")
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.dataframe(df, use_container_width=True)

    if st.button("📄 Générer le rapport final"):
        st.markdown(f"### 📌 Rapport final pour {nom}, {age} ans")

        for parcours_type in df["Parcours"].unique():
            sous_df = df[df["Parcours"] == parcours_type]
            if not sous_df.empty:
                st.markdown(f"#### 🏃 {parcours_type}")
                st.dataframe(sous_df[["Temps (s)"]])

                temps_moyen = sous_df["Temps (s)"].mean()
                st.markdown(f"- **Temps moyen :** {temps_moyen:.2f} secondes")

                # Analyse de performance
                st.markdown("### 🧠 Analyse automatique")

                if parcours_type.startswith("Parcours Zig-Zag"):
                    # Références académies pour Zig-Zag 15m
                    if temps_moyen < 6:
                        st.markdown("- ✅ **Conduite très rapide** – excellent niveau technique.")
                    elif 6 <= temps_moyen <= 8:
                        st.markdown("- ⚠️ **Conduite correcte** – potentiel d'amélioration.")
                    else:
                        st.markdown("- ❌ **Conduite lente** – travailler sur l'explosivité et la précision.")
                else:
                    # Références pour Courbe (environ 18m)
                    if temps_moyen < 8:
                        st.markdown("- ✅ **Conduite rapide et fluide** – très bon contrôle.")
                    elif 8 <= temps_moyen <= 10:
                        st.markdown("- ⚠️ **Conduite moyenne** – travailler la régularité.")
                    else:
                        st.markdown("- ❌ **Temps élevé** – manque de maîtrise sous pression.")

                # Plan d'action recommandé
                st.markdown("### 🎯 Plan d'action recommandé")
                if (parcours_type.startswith("Parcours Zig-Zag") and temps_moyen > 8) or (parcours_type.startswith("Parcours Courbe") and temps_moyen > 10):
                    st.markdown("""
#### 🟥 Niveau Prioritaire – Amélioration urgente

**Objectif :** Améliorer la vitesse et le contrôle en conduite.  
**Exercices :**
- Conduite rapide entre plots (15m)
- Conduite avec changement de rythme
- Duel 1v1 avec sortie rapide

**Fréquence :** 3x par semaine pendant 4 semaines  
**Objectif :** Réduire le temps moyen à < 7s (Zig-Zag) ou < 9s (Courbe)
                    """)
                elif temps_moyen <= 10:
                    st.markdown("""
#### 🟨 Niveau Modéré – Consolidation

**Objectif :** Stabiliser la maîtrise du ballon à vitesse modérée.  
**Exercices :**
- Conduite avec arrêts brusques
- Variations de surface de contact (intérieur/extérieur)
- Petits jeux en espace réduit

**Fréquence :** 2x par semaine pendant 3 semaines  
**Objectif :** Maintenir la qualité sous pression
                    """)
                else:
                    st.markdown("""
#### 🟩 Niveau Avancé – Maintien

**Objectif :** Transfert de la conduite rapide vers les matchs.  
**Exercices :**
- Jeu à thème avec contrainte de temps
- Enchaînement dribble - passe
- Analyse vidéo et autocorrection

**Fréquence :** 1x par semaine  
**Objectif :** Transfert vers la performance réelle
                    """)



