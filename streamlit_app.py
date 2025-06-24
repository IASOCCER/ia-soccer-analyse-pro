import streamlit as st
import pandas as pd

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.title("⚽ IA Soccer – Analyse Technique des Joueurs")

# Menu principal
menu = st.sidebar.selectbox("Choisissez un test :", ["Test de passe", "Conduite de balle – Zigzag", "Conduite de balle – Ligne droite"])

# Initialiser les données
if "tests" not in st.session_state:
    st.session_state["tests"] = []

# Formulaire joueur (utilisé dans tous les tests)
st.sidebar.markdown("### Informations du joueur")
nom = st.sidebar.text_input("Nom du joueur")
age = st.sidebar.number_input("Âge", min_value=8, max_value=18, step=1)

# === TEST DE PASSE ===
if menu == "Test de passe":
    st.header("🎯 Test de Passe avec IA")

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
            temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if nb_acertes > 0 else 0.0

            st.session_state["tests"].append({
                "Nom": nom,
                "Âge": age,
                "Test": "Passe",
                "Pied": pied,
                "Pression": pression,
                "Précision (%)": precision,
                "Temps moyen (s)": temps_moyen
            })
            st.success("✅ Test de passe ajouté avec succès!")
        else:
            st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

# === CONDUITE DE BALLE – ZIGZAG ===
elif menu == "Conduite de balle – Zigzag":
    st.header("🔀 Test de Conduite de Balle – Zigzag")
    distance = st.selectbox("Distance totale", ["15 mètres", "20 mètres"])
    temps = st.number_input("Temps réalisé (en secondes)", min_value=0.0, max_value=30.0, step=0.1)

    if st.button("➕ Ajouter ce test zigzag"):
        if nom and age:
            st.session_state["tests"].append({
                "Nom": nom,
                "Âge": age,
                "Test": "Conduite Zigzag",
                "Distance": distance,
                "Temps (s)": temps
            })
            st.success("✅ Test ajouté avec succès!")
        else:
            st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

# === CONDUITE DE BALLE – LIGNE DROITE ===
elif menu == "Conduite de balle – Ligne droite":
    st.header("📏 Test de Conduite de Balle – Ligne Droite")
    distance_ld = st.selectbox("Distance totale", ["10 mètres", "15 mètres"])
    temps_ld = st.number_input("Temps réalisé (en secondes)", min_value=0.0, max_value=20.0, step=0.1, key="ligne_droite")

    if st.button("➕ Ajouter ce test ligne droite"):
        if nom and age:
            st.session_state["tests"].append({
                "Nom": nom,
                "Âge": age,
                "Test": "Conduite Ligne Droite",
                "Distance": distance_ld,
                "Temps (s)": temps_ld
            })
            st.success("✅ Test ajouté avec succès!")
        else:
            st.warning("Veuillez remplir toutes les informations pour ajouter le test.")

# === AFFICHAGE DES TESTS ===
if st.session_state["tests"]:
    st.markdown("### 📊 Tous les tests enregistrés")
    df = pd.DataFrame(st.session_state["tests"])
    st.dataframe(df, use_container_width=True)

    if st.button("📄 Générer les rapports"):
        st.markdown(f"### 📌 Rapport pour {nom}, {age} ans")

        # Rapport – Test de passe
        df_passe = df[df["Test"] == "Passe"]
        if not df_passe.empty:
            for pied_type in ["Pied gauche", "Pied droit"]:
                sous_df = df_passe[df_passe["Pied"] == pied_type]
                if not sous_df.empty:
                    st.markdown(f"#### 🦶 Passe – {pied_type}")
                    st.dataframe(sous_df[["Pression", "Précision (%)", "Temps moyen (s)"]])

                    precision_moy = sous_df["Précision (%)"].mean()
                    temps_moy = sous_df["Temps moyen (s)"].mean()

                    st.markdown(f"- **Précision moyenne :** {precision_moy:.1f}%")
                    st.markdown(f"- **Temps moyen de réaction :** {temps_moy:.2f} s")

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

        # Rapport – Conduite de balle (zigzag et ligne droite)
        for test_type in ["Conduite Zigzag", "Conduite Ligne Droite"]:
            df_cond = df[df["Test"] == test_type]
            if not df_cond.empty:
                st.markdown(f"#### 🚀 {test_type}")
                st.dataframe(df_cond[["Distance", "Temps (s)"]])

                temps_moyen = df_cond["Temps (s)"].mean()
                st.markdown(f"- **Temps moyen :** {temps_moyen:.2f} s")

                st.markdown("### 🧠 Analyse automatique")
                if temps_moyen <= 6:
                    st.markdown("- ✅ **Très rapide** – excellente maîtrise.")
                elif 6 < temps_moyen <= 8:
                    st.markdown("- ⚠️ **Temps modéré** – bonne base, à optimiser.")
                else:
                    st.markdown("- ❌ **Temps élevé** – besoin de travail technique et coordination.")

                st.markdown("### 🎯 Plan d'action recommandé")
                if temps_moyen > 8:
                    st.markdown("""
#### 🟥 Niveau Prioritaire

**Objectif :** Améliorer la vitesse et le contrôle de balle.  
**Exercices :**
- Conduite balle proche en zigzag
- Slalom rapide chronométré
- Jeux réduits avec transitions
                    """)
                elif 6 < temps_moyen <= 8:
                    st.markdown("""
#### 🟨 Niveau Modéré

**Objectif :** Optimiser l'efficacité technique.  
**Exercices :**
- Conduite sur 15m avec obstacles
- Travail en duo avec pression
- Changement de rythme avec ballon
                    """)
                else:
                    st.markdown("""
#### 🟩 Niveau Avancé

**Objectif :** Transfert vers match réel.  
**Exercices :**
- Jeu libre avec touche limitée
- Conduite + passe décisive
- Vidéo feedback
                    """)


    if st.button("➕ Ajouter ce test", key="ajouter_circuit"):
        st.success(f"Test enregistré: {nom}, {age} ans, {temps}s")


