
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.title("IA Soccer Analyse Pro – Évaluation complète")

# Chargement des données précédentes
fichier = "joueurs.csv"
if os.path.exists(fichier):
    df = pd.read_csv(fichier)
else:
    df = pd.DataFrame(columns=[
        "Nom", "Âge", "Temps de passe (s)", "Précision passe (%)",
        "Vitesse tir (km/h)", "Précision tir (%)", "Taille (cm)",
        "Poids (kg)", "Masse musculaire (%)", "IMC"
    ])

st.markdown("### ➕ Ajouter un joueur")

nom = st.text_input("Nom du joueur")
age = st.number_input("Âge", min_value=8, max_value=18)

# Évaluation technique
temps_passe = st.number_input("Temps moyen de passe (en secondes)", value=3.0)
precision_passe = st.slider("Précision du passe (%)", 0, 100, 90)
vitesse_tir = st.number_input("Vitesse du tir (km/h)", value=65.0)
precision_tir = st.slider("Précision du tir (%)", 0, 100, 60)

# Évaluation biométrique
taille = st.number_input("Taille (en cm)", value=140)
poids = st.number_input("Poids (en kg)", value=40)
masse_musculaire = st.slider("Masse musculaire estimée (%)", 0, 100, 45)
taille_m = taille / 100
imc = round(poids / (taille_m ** 2), 1)

if st.button("✅ Sauvegarder le joueur"):
    nouvelle_ligne = {
        "Nom": nom,
        "Âge": age,
        "Temps de passe (s)": temps_passe,
        "Précision passe (%)": precision_passe,
        "Vitesse tir (km/h)": vitesse_tir,
        "Précision tir (%)": precision_tir,
        "Taille (cm)": taille,
        "Poids (kg)": poids,
        "Masse musculaire (%)": masse_musculaire,
        "IMC": imc
    }
    df = df.append(nouvelle_ligne, ignore_index=True)
    df.to_csv(fichier, index=True)
    st.success("✅ Joueur sauvegardé avec succès!")

st.markdown("---")
st.markdown("### 📋 Liste des joueurs enregistrés")

if not df.empty:
    st.dataframe(df)

    st.download_button(
        label="📥 Télécharger en CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='joueurs_iasoccer.csv',
        mime='text/csv'
    )
else:
    st.info("Aucun joueur enregistré pour le moment.")
