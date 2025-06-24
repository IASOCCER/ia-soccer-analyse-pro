import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro – Conduite de Balle", layout="wide")
st.title("🏃 IA Soccer – Analyse de la Conduite de Balle")

# Distances approximatives des parcours
distance_map = {
    "Parcours Zig-Zag (6 plots en ligne, 2,5m entre chaque)": 15.0,
    "Parcours Courbe (3 courbes autour de 3 plots écartés de 4m)": 18.0
}

# Initialisation de la mémoire
if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

st.markdown("### 👨‍🎓 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

st.markdown("### 🚧 Détails du test de conduite de balle")
parcours = st.selectbox("Type de parcours", list(distance_map.keys()))
temps_total = st.number_input("Temps total pour compléter le parcours (en secondes)", min_value=1.0, max_value=30.0, step=0.1)

if st.button("➕ Ajouter ce test de conduite"):
    if nom and age:
        distance = distance_map.get(parcours, None)
        st.session_state["conduite_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Parcours": parcours,
            "Distance (m)": distance,
            "Temps (s)": temps_total
        })
        st.success("✅ Test ajouté avec succès!")
    else:
        st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

if st.session_state["conduite_tests"]:
    st.markdown("### 📊 Tests enregistrés")
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.dataframe(df, use_container_width=True)

    if st.button("📄 Générer le rapport final"):
        st.markdown(f"### 📌 Rapport final pour {nom}, {age} ans")

        for parcours_type in df["Parcours"].unique():
            sous_df = df[df["Parcours"] == parcours_type]
            if not sous_df.empty:
                distance = distance_map.get(parcours_type, None)
                st.markdown(f"#### 🏃 {parcours_type} – ~{distance} m")
                st.dataframe(sous_df[["Temps (s)", "Distance (m)"]])

                temps_moyen = sous_df["Temps (s)"].mean()
                vitesse = round(distance / temps_moyen, 2) if temps_moyen > 0 else 0

                st.markdown(f"- **Distance du parcours :** ~{distance} m")
                st.markdown(f"- **Temps moyen :** {temps_moyen:.2f} s")
                st.markdown(f"- **Vitesse moyenne :** {vitesse:.2f} m/s")

                # Analyse
                st.markdown("### 🧐 Analyse automatique")
                if parcours_type.startswith("Parcours Zig-Zag"):
                    if temps_moyen < 6:
                        st.markdown("- ✅ **Conduite très rapide** – excellent niveau technique.")
                    elif 6 <= temps_moyen <= 8:
                        st.markdown("- ⚠️ **Conduite correcte** – potentiel d'amélioration.")
                    else:
                        st.markdown("- ❌ **Conduite lente** – travailler sur l'explositivité et la précision.")
                else:
                    if temps_moyen < 8:
                        st.markdown("- ✅ **Conduite rapide et fluide** – très bon contrôle.")
                    elif 8 <= temps_moyen <= 10:
                        st.markdown("- ⚠️ **Conduite moyenne** – travailler la régularité.")
                    else:
                        st.markdown("- ❌ **Temps élevé** – manque de maîtrise sous pression.")

                # Plan d'action
                st.markdown("### 🌟 Plan d'action recommandé")
                if (parcours_type.startswith("Parcours Zig-Zag") and temps_moyen > 8) or (parcours_type.startswith("Parcours Courbe") and temps_moyen > 10):
                    st.markdown("""
#### 🔵 Niveau Prioritaire – Amélioration urgente

**Objectif :** Améliorer la vitesse et le contrôle en conduite.  
**Exercices :**
- Conduite rapide entre plots (15m)  
- Conduite avec changement de rythme  
- Duel 1v1 avec sortie rapide

**Fréquence :** 3x/semaine pendant 4 semaines  
**Objectif :** Atteindre < 7s (Zig-Zag) ou < 9s (Courbe)
                    """)
                elif temps_moyen <= 10:
                    st.markdown("""
#### 🔶 Niveau Modéré – Consolidation

**Objectif :** Stabiliser la maîtrise du ballon à vitesse modérée.  
**Exercices :**
- Conduite avec arrêts brusques  
- Variations de surface de contact (intérieur/extérieur)  
- Petits jeux en espace réduit

**Fréquence :** 2x/semaine pendant 3 semaines  
**Objectif :** Maintien au-dessus du niveau cible
                    """)
                else:
                    st.markdown("""
#### 🔹 Niveau Avancé – Maintien

**Objectif :** Transfert de la conduite rapide vers les matchs.  
**Exercices :**
- Jeu réduit à thème avec contrainte de temps  
- Enchaînement conduite + passe  
- Vidéo feedback et correction technique

**Fréquence :** 1 session/semaine  
**Objectif :** Continuité de performance en match
                    """)

