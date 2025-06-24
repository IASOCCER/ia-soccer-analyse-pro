import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer – Conduite de Balle", layout="wide")
st.title("⚡ IA Soccer – Analyse de la Conduite de Balle")

# Initialisation
if "conduite_tests" not in st.session_state:
    st.session_state["conduite_tests"] = []

# 🔍 Fonction IA – Analyse et plan d'action
def evaluer_conduite(type_parcours, age, temps):
    if type_parcours == "Zig-Zag":
        ref = 8.0 if age <= 12 else 7.0
    else:
        ref = 9.5 if age <= 12 else 8.5

    diff = temps - ref

    if diff <= -1:
        note = "🟩 Avancé"
        plan = """
**Objectif :** Transférer la vitesse de conduite vers des situations de match.  
**Exercices :**
- Conduite avec opposition passive
- Enchaînement conduite + passe rapide
- Vidéo feedback sur posture
        """
    elif -1 < diff <= 1:
        note = "🟨 Correct"
        plan = """
**Objectif :** Gagner en fluidité et coordination.  
**Exercices :**
- Slalom chronométré (3 séries)
- Changement de rythme à mi-parcours
- Travail de prise d'information visuelle
        """
    else:
        note = "🟥 À améliorer"
        plan = """
**Objectif :** Maîtriser le ballon en pleine vitesse.  
**Exercices :**
- Conduite à faible vitesse avec contrôle du regard
- Parcours avec plots rapprochés (1,5m)
- Reprise technique avec vidéo (2x/sem)
        """
    return note, plan.strip()

# 🧑 Informations
st.markdown("### 👤 Informations sur le joueur")
nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18, step=1)

st.markdown("### 🛣️ Type de parcours")
type_parcours = st.selectbox("Sélectionner le type", ["Zig-Zag (6 cônes – 2,5m)", "Changement de direction (4 virages)"])
type_parcours_simple = "Zig-Zag" if "Zig-Zag" in type_parcours else "Changement"

st.markdown("### ⏱️ Temps total")
temps = st.number_input("Temps réalisé (en secondes)", min_value=0.0, step=0.01)

# ➕ Ajouter
if st.button("➕ Ajouter ce test"):
    if nom and temps > 0:
        note, plan = evaluer_conduite(type_parcours_simple, age, temps)
        st.session_state["conduite_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Type": type_parcours_simple,
            "Temps (s)": temps,
            "Évaluation": note,
            "Plan d'action": plan
        })
        st.success("✅ Test ajouté avec succès.")
    else:
        st.warning("Veuillez remplir tous les champs.")

# 📊 Affichage
if st.session_state["conduite_tests"]:
    st.markdown("### 📊 Résultats enregistrés")
    df = pd.DataFrame(st.session_state["conduite_tests"])
    st.dataframe(df[["Nom", "Âge", "Type", "Temps (s)", "Évaluation"]], use_container_width=True)

    if st.button("📄 Générer le rapport complet"):
        for entry in st.session_state["conduite_tests"]:
            st.markdown(f"---\n### 🧠 Rapport – {entry['Nom']} ({entry['Âge']} ans) – {entry['Type']}")
            st.markdown(f"- **Temps :** {entry['Temps (s)']} s")
            st.markdown(f"- **Évaluation :** {entry['Évaluation']}")
            st.markdown("### 🎯 Plan d'action recommandé")
            st.markdown(entry["Plan d'action"])





