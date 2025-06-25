import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# CLIENTE OPENAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# CONFIGURAÇÃO GERAL
st.set_page_config(page_title="IA Soccer Analyse Pro", layout="wide")
st.sidebar.image("https://iasoccer.com/wp-content/uploads/2024/09/IA-SOCCER-FC-PORTO-WHITE.png", width=250)
st.sidebar.title("IA Soccer Analyse Pro")

# MENU LATERAL
page = st.sidebar.selectbox("Choisissez une section :", [
    "🏠 Accueil",
    "🧍 Joueur",
    "🎯 Passe",
    "🛞 Conduite",
    "⚽ Remate",
    "🏃‍♂️ Sprint",
    "🚀 Agilité",
    "💪 Masse musculaire",
    "📊 Rapport Global"
])

# DADOS DO JOGADOR
if "joueur" not in st.session_state:
    st.session_state["joueur"] = {}

# FUNÇÃO GERAL DE VERIFICAÇÃO
def verifier_joueur():
    if not st.session_state["joueur"]:
        st.warning("Veuillez d'abord remplir les informations du joueur dans l'onglet 🧍 Joueur.")
        st.stop()
# ACCUEIL
if page == "🏠 Accueil":
    st.title("Bienvenue à IA Soccer Analyse Pro ⚽")
    st.markdown("Cette plateforme permet d'évaluer la performance technique et physique des joueurs de 8 à 18 ans.")
    st.info("🧠 Chaque test utilise l'intelligence artificielle pour générer une analyse et un plan d'action professionnel.")

# CADASTRO DO JOGADOR
elif page == "🧍 Joueur":
    st.title("🧍 Informations du Joueur")
    nom = st.text_input("Nom complet")
    age = st.number_input("Âge", min_value=8, max_value=18)
    if st.button("✅ Enregistrer"):
        st.session_state["joueur"] = {"nom": nom, "âge": age}
        st.success("Informations du joueur enregistrées.")
elif page == "🎯 Passe":
    verifier_joueur()
    st.title("🎯 Analyse du Passe – IA Soccer")

    if "tests_passe" not in st.session_state:
        st.session_state["tests_passe"] = []

    pied = st.selectbox("Pied utilisé", ["Pied gauche", "Pied droit"])
    pression = st.selectbox("Niveau de pression", ["Faible (12s)", "Moyenne (6s)", "Élevée (3s)"])
    nb_acertes = st.slider("Passes réussies sur 6", 0, 6, 3)

    temps_reactions = []
    if nb_acertes > 0:
        st.markdown("Temps de réaction pour chaque passe réussie :")
        for i in range(1, nb_acertes + 1):
            t = st.number_input(f"Temps passe {i}", 0.0, 15.0, step=0.1, key=f"passe_{i}")
            temps_reactions.append(t)

    if st.button("➕ Ajouter ce test de passe"):
        precision = round((nb_acertes / 6) * 100, 1)
        temps_moyen = round(sum(temps_reactions) / len(temps_reactions), 2) if nb_acertes > 0 else 0.0

        test = {
            "Nom": st.session_state["joueur"]["nom"],
            "Âge": st.session_state["joueur"]["âge"],
            "Pied": pied,
            "Pression": pression,
            "Précision (%)": precision,
            "Temps moyen (s)": temps_moyen
        }
        st.session_state["tests_passe"].append(test)
        st.success("✅ Test ajouté avec succès.")

    if st.session_state["tests_passe"]:
        st.markdown("### 📊 Résultats enregistrés")
        df = pd.DataFrame(st.session_state["tests_passe"])
        st.dataframe(df, use_container_width=True)

        if st.button("📄 Rapport IA"):
            pied_types = ["Pied gauche", "Pied droit"]
            for pied_type in pied_types:
                sous_df = df[df["Pied"] == pied_type]
                if not sous_df.empty:
                    st.markdown(f"#### 🦶 {pied_type}")
                    st.dataframe(sous_df[["Pression", "Précision (%)", "Temps moyen (s)"]])

                    precision_moy = sous_df["Précision (%)"].mean()
                    temps_moy = sous_df["Temps moyen (s)"].mean()

                    st.markdown(f"- **Précision moyenne :** {precision_moy:.1f}%")
                    st.markdown(f"- **Temps moyen :** {temps_moy:.2f} s")

                    st.markdown("### 🧠 Analyse automatique")
                    if precision_moy >= 70:
                        st.success("- ✅ Précision élevée – bon contrôle.")
                    elif 50 <= precision_moy < 70:
                        st.warning("- ⚠️ Précision moyenne – amélioration possible.")
                    else:
                        st.error("- ❌ Faible précision – à travailler.")

                    if temps_moy < 4:
                        st.success("- ✅ Réaction rapide – très bon.")
                    elif 4 <= temps_moy <= 6:
                        st.warning("- ⚠️ Réaction moyenne.")
                    else:
                        st.error("- ❌ Réaction lente – s'entraîner sous pression.")

                    st.markdown("### 🎯 Plan d'action recommandé")
                    if precision_moy < 60 or temps_moy > 6:
                        st.markdown("- **Objectif :** Réduire le temps de réaction et améliorer la précision.")
                    elif 60 <= precision_moy < 70 or 4 <= temps_moy <= 6:
                        st.markdown("- **Objectif :** Consolider la régularité sous pression.")
                    else:
                        st.markdown("- **Objectif :** Transférer la qualité de passe au match réel.")
elif page == "🛞 Conduite":
    verifier_joueur()
    st.title("🛞 Analyse de la Conduite de Balle")

    if "conduite_tests" not in st.session_state:
        st.session_state["conduite_tests"] = []

    parcours = st.selectbox("Type de parcours", [
        "Zig-Zag (6 cônes, 15m)", "Changements de Direction (3 virages, 12m)"
    ])
    temps = st.number_input("⏱️ Temps (secondes)", min_value=0.0, step=0.1)
    perte_controle = False
    if parcours.startswith("Changements"):
        perte_controle = st.radio("❌ Perte de contrôle de la balle ?", ["Non", "Oui"]) == "Oui"

    # Níveis por idade
    zigzag_ref = {
        8: 11.5, 9: 11.0, 10: 10.5, 11: 10.0, 12: 9.6, 13: 9.2,
        14: 8.9, 15: 8.6, 16: 8.4, 17: 8.2, 18: 8.0
    }

    change_ref = {
        8: {"moyen": 16, "excellent": 14, "faible": 20},
        9: {"moyen": 15, "excellent": 13, "faible": 19},
        10: {"moyen": 14, "excellent": 12, "faible": 18},
        11: {"moyen": 13, "excellent": 11, "faible": 17},
        12: {"moyen": 12, "excellent": 10, "faible": 16},
        13: {"moyen": 11, "excellent": 9, "faible": 15},
        14: {"moyen": 10.5, "excellent": 8.5, "faible": 14.5},
        15: {"moyen": 10, "excellent": 8, "faible": 14},
        16: {"moyen": 9.5, "excellent": 7.5, "faible": 13.5},
        17: {"moyen": 9, "excellent": 7, "faible": 13},
        18: {"moyen": 9, "excellent": 7, "faible": 13}
    }

    def analyser_niveau(age, temps, parcours):
        if parcours.startswith("Zig-Zag"):
            ref = zigzag_ref.get(age, 10.0)
            if temps <= ref - 1.0:
                return "Excellent"
            elif temps <= ref + 1.0:
                return "Bon"
            elif temps <= ref + 3.0:
                return "Régulier"
            else:
                return "Faible"
        else:
            ref = change_ref.get(age, {"moyen": 12, "excellent": 10, "faible": 16})
            if temps <= ref["excellent"]:
                return "Excellent"
            elif temps >= ref["faible"]:
                return "Faible"
            elif temps <= ref["moyen"]:
                return "Bon"
            else:
                return "Régulier"

    def generer_plan_ia(nom, age, parcours, temps, perte_controle, niveau):
        prompt = f"""
Le joueur s'appelle {nom}, {age} ans.
Exercice : {parcours}
Temps : {temps} s — Niveau évalué : {niveau}
Perte de contrôle : {"Oui" if perte_controle else "Non"}

Agis comme un entraîneur de haut niveau.
Crée un plan d'action personnalisé selon le niveau, l'âge et le type de parcours.
Inclue :
- Un commentaire technique
- 2 exercices recommandés
- Plan sur 7 jours
- Conseils d'amélioration

Réponds en 5 lignes maximum.
"""
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Erreur lors de l'appel à l'IA : {str(e)}"

    if st.button("➕ Ajouter ce test de conduite"):
        age = st.session_state["joueur"]["âge"]
        nom = st.session_state["joueur"]["nom"]
        niveau = analyser_niveau(age, temps, parcours)
        analyse = generer_plan_ia(nom, age, parcours, temps, perte_controle, niveau)

        st.session_state["conduite_tests"].append({
            "Nom": nom,
            "Âge": age,
            "Parcours": parcours,
            "Temps (s)": temps,
            "Perte de Contrôle": "Oui" if perte_controle else "Non",
            "Niveau": niveau,
            "Analyse IA": analyse
        })
        st.success(f"✅ Test ajouté avec succès. Niveau: {niveau}")
        st.markdown(f"### 🧠 Analyse IA\n\n{analyse}")

    if st.session_state["conduite_tests"]:
        st.markdown("### 📋 Résultats enregistrés")
        df = pd.DataFrame(st.session_state["conduite_tests"])
        st.dataframe(df, use_container_width=True)
elif page == "⚽ Remate":
    verifier_joueur()
    st.title("⚽ Analyse du Remate Technique avec IA")

    if "tests_remate" not in st.session_state:
        st.session_state["tests_remate"] = []

    nom = st.session_state["joueur"]["nom"]
    age = st.session_state["joueur"]["âge"]

    # 🎯 Pied droit
    st.markdown("### 🦵 Pied Droit")
    precision_d = st.slider("🎯 Précision (sur 10 tirs)", 0, 10, 0, key="precision_d")
    vitesses_d = [st.number_input(f"Vitesse Tir {i+1} (km/h)", 0.0, 200.0, step=0.1, key=f"v_d{i}") for i in range(10)]
    vitesse_d_moy = round(sum(vitesses_d) / 10, 2)

    # 🎯 Pied gauche
    st.markdown("### 🦵 Pied Gauche")
    precision_g = st.slider("🎯 Précision (sur 10 tirs)", 0, 10, 0, key="precision_g")
    vitesses_g = [st.number_input(f"Vitesse Tir {i+1} (km/h)", 0.0, 200.0, step=0.1, key=f"v_g{i}") for i in range(10)]
    vitesse_g_moy = round(sum(vitesses_g) / 10, 2)

    # Referência por idade
    base_ref = {
        10: {"precision": 50, "vitesse": 45},
        11: {"precision": 55, "vitesse": 50},
        12: {"precision": 60, "vitesse": 55},
        13: {"precision": 65, "vitesse": 60},
        14: {"precision": 70, "vitesse": 65},
        15: {"precision": 75, "vitesse": 70},
        16: {"precision": 80, "vitesse": 75},
        17: {"precision": 85, "vitesse": 80},
        18: {"precision": 90, "vitesse": 85},
    }

    def generer_analyse_remate(nom, age, precision_d, precision_g, vitesse_d, vitesse_g):
        ref = base_ref.get(age, {"precision": 65, "vitesse": 60})
        precision_moy = (precision_d + precision_g) / 2
        vitesse_moy = (vitesse_d + vitesse_g) / 2
        ecart_precision = round(precision_moy - ref["precision"], 1)
        ecart_vitesse = round(vitesse_moy - ref["vitesse"], 1)

        comparaison = f"""
### 📈 Comparaison avec les standards pour {age} ans :
- Précision moyenne : {precision_moy:.1f}% (écart de {ecart_precision:+.1f}%)
- Vitesse moyenne : {vitesse_moy:.1f} km/h (écart de {ecart_vitesse:+.1f} km/h)
"""

        prompt = f"""
{comparaison}

Fais une analyse technique complète des tirs de ce joueur ({nom}, {age} ans).
Puis, propose un plan d'action personnalisé avec 3 à 5 conseils concrets pour améliorer sa puissance, sa précision et sa posture.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un entraîneur professionnel spécialisé en analyse technique du football."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            return comparaison + "\n" + response.choices[0].message.content
        except Exception as e:
            if "authentication" in str(e).lower():
                return "❌ Erreur d'authentification – vérifie ta clé API OpenAI."
            return f"❌ Une erreur est survenue : {e}"

    if st.button("✅ Ajouter ce test"):
        analyse = generer_analyse_remate(
            nom, age,
            precision_d * 10, precision_g * 10,
            vitesse_d_moy, vitesse_g_moy
        )

        test = {
            "Nom": nom,
            "Âge": age,
            "Précision Droit (%)": precision_d * 10,
            "Précision Gauche (%)": precision_g * 10,
            "Vitesse Moy. Droit (km/h)": vitesse_d_moy,
            "Vitesse Moy. Gauche (km/h)": vitesse_g_moy,
            "Analyse IA": analyse
        }

        st.session_state["tests_remate"].append(test)
        st.success("✅ Test enregistré avec succès !")

    if st.session_state["tests_remate"]:
        st.markdown("### 📊 Résultat du dernier test")
        dernier = st.session_state["tests_remate"][-1]
        st.dataframe(pd.DataFrame([dernier]))

        st.markdown("### 🧠 Analyse IA")
        st.markdown(dernier["Analyse IA"])
elif page == "🏃‍♂️ Sprint":
    verifier_joueur()
    st.title("🏃‍♂️ Analyse du Sprint – IA Soccer")

    if "sprint_tests" not in st.session_state:
        st.session_state["sprint_tests"] = []

    nom = st.session_state["joueur"]["nom"]
    age = st.session_state["joueur"]["âge"]

    type_sprint = st.selectbox("Type de sprint", ["Sprint 10m", "Sprint 20m"])
    temps = st.number_input("Temps réalisé (secondes)", min_value=0.0, step=0.01)

    def get_reference(age, type_sprint):
        if type_sprint == "Sprint 10m":
            if age <= 10: return {"excellent": 2.2, "bon": 2.7}
            elif age <= 12: return {"excellent": 2.0, "bon": 2.5}
            elif age <= 14: return {"excellent": 1.9, "bon": 2.4}
            elif age <= 16: return {"excellent": 1.8, "bon": 2.3}
            else: return {"excellent": 1.7, "bon": 2.2}
        else:
            if age <= 10: return {"excellent": 4.2, "bon": 4.8}
            elif age <= 12: return {"excellent": 4.0, "bon": 4.6}
            elif age <= 14: return {"excellent": 3.8, "bon": 4.4}
            elif age <= 16: return {"excellent": 3.6, "bon": 4.2}
            else: return {"excellent": 3.4, "bon": 4.0}

    def evaluer_sprint(age, type_sprint, temps):
        ref = get_reference(age, type_sprint)
        note = 100
        if temps <= ref["excellent"]:
            niveau = "Excellent"
        elif temps <= ref["bon"]:
            note -= 15
            niveau = "Bon"
        else:
            note -= 30
            niveau = "À améliorer"
        return niveau, note, ref

    def generer_analyse_sprint(age, type_sprint, temps, niveau):
        prompt = f"""
Un joueur de {age} ans a effectué un test de sprint de type '{type_sprint}' et a réalisé un temps de {temps:.2f} secondes. 
Niveau évalué : {niveau}.

1. Fournis une évaluation professionnelle en français.
2. Donne une explication sur sa performance selon l'âge et la distance.
3. Propose un plan d'action clair et personnalisé pour améliorer son sprint.

Sois concis, structuré et professionnel.
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un coach de football spécialisé en performance physique."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur IA : {str(e)}"

    if st.button("➕ Ajouter ce test de sprint"):
        niveau, note, ref = evaluer_sprint(age, type_sprint, temps)
        analyse = generer_analyse_sprint(age, type_sprint, temps, niveau)
        test = {
            "nom": nom,
            "âge": age,
            "type": type_sprint,
            "temps": temps,
            "niveau": niveau,
            "note": note,
            "réf": ref,
            "analyse": analyse,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        st.session_state["sprint_tests"].append(test)
        st.success("✅ Test ajouté avec succès.")

    if st.session_state["sprint_tests"]:
        st.markdown("### 📊 Tests enregistrés")
        for i, t in enumerate(st.session_state["sprint_tests"]):
            st.write(f"**Test {i+1} – {t['date']}**")
            st.write(f"👤 {t['nom']} | Âge: {t['âge']} | Type: {t['type']}")
            st.write(f"⏱️ Temps: {t['temps']} s | Référence: Excellent ≤ {t['réf']['excellent']}s / Bon ≤ {t['réf']['bon']}s")
            st.write(f"📈 Note: {t['note']} /100 – Niveau: **{t['niveau']}**")
            st.markdown(f"🧠 **Analyse IA** :\n\n{t['analyse']}")
            st.markdown("---")
elif page == "💪 Masse musculaire":
    verifier_joueur()
    st.title("💪 Évaluation de la Masse Musculaire – IA Soccer")

    if "muscle_tests" not in st.session_state:
        st.session_state["muscle_tests"] = []

    nom = st.session_state["joueur"]["nom"]
    age = st.session_state["joueur"]["âge"]

    poids = st.number_input("⚖️ Poids total (kg)", min_value=10.0, step=0.1)
    masse_musculaire = st.number_input("💪 Masse musculaire (kg)", min_value=5.0, step=0.1)

    def get_reference_muscle(age):
        if age <= 10:
            return {"excellent": 20, "bon": 16}
        elif age <= 12:
            return {"excellent": 25, "bon": 20}
        elif age <= 14:
            return {"excellent": 30, "bon": 25}
        elif age <= 16:
            return {"excellent": 35, "bon": 30}
        else:
            return {"excellent": 40, "bon": 34}

    def evaluer_muscle(age, masse):
        ref = get_reference_muscle(age)
        note = 100
        if masse >= ref["excellent"]:
            niveau = "Excellent"
        elif masse >= ref["bon"]:
            note -= 15
            niveau = "Bon"
        else:
            note -= 30
            niveau = "À améliorer"
        return niveau, note, ref

    def generer_analyse_muscle(nom, age, poids, masse, niveau):
        pourcentage = (masse / poids) * 100
        prompt = f"""
Le joueur {nom}, âgé de {age} ans, a été évalué avec une masse musculaire de {masse:.1f} kg sur un poids total de {poids:.1f} kg, soit environ {pourcentage:.1f}% de masse musculaire. Son niveau a été classé : {niveau}.

Fournis une analyse professionnelle de sa composition corporelle et un plan d'action personnalisé pour améliorer sa masse musculaire et sa condition physique. Inclure si pertinent des suggestions nutritionnelles et de renforcement musculaire.

Réponds en français de façon structurée, claire et adaptée à son âge.
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un préparateur physique expert en jeunes athlètes de football."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Erreur IA : {str(e)}"

    if st.button("➕ Ajouter ce test"):
        niveau, note, ref = evaluer_muscle(age, masse_musculaire)
        analyse = generer_analyse_muscle(nom, age, poids, masse_musculaire, niveau)
        test = {
            "nom": nom,
            "âge": age,
            "poids": poids,
            "masse_musculaire": masse_musculaire,
            "niveau": niveau,
            "note": note,
            "réf": ref,
            "analyse": analyse,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        st.session_state["muscle_tests"].append(test)
        st.success("✅ Test ajouté avec succès.")

    if st.session_state["muscle_tests"]:
        st.markdown("### 📊 Tests enregistrés")
        for i, t in enumerate(st.session_state["muscle_tests"]):
            pourcent = (t['masse_musculaire'] / t['poids']) * 100
            st.write(f"**Test {i+1} – {t['date']}**")
            st.write(f"👤 {t['nom']} | Âge: {t['âge']}")
            st.write(f"⚖️ Masse musculaire: {t['masse_musculaire']} kg / {t['poids']} kg ({pourcent:.1f}%)")
            st.write(f"📈 Note: {t['note']} /100 – Niveau: **{t['niveau']}**")
            st.markdown(f"🧠 **Analyse IA** :\n\n{t['analyse']}")
            st.markdown("---")
elif page == "📊 Rapport Global":
    verifier_joueur()
    st.title("📊 Rapport Global du Joueur")

    nom = st.session_state["joueur"]["nom"]
    age = st.session_state["joueur"]["âge"]

    st.markdown(f"### 👤 Joueur : **{nom}** – Âge : **{age} ans**")

    def afficher_section(titre, tests, colonnes):
        st.markdown(f"#### 📌 {titre}")
        if tests:
            df = pd.DataFrame(tests)
            st.dataframe(df[colonnes], use_container_width=True)
        else:
            st.info(f"Aucun test enregistré pour **{titre}**.")

    # Résumé pour chaque test
    afficher_section("🎯 Passe", st.session_state.get("tests_passe", []), ["Pied", "Pression", "Précision (%)", "Temps moyen (s)"])
    afficher_section("🛞 Conduite", st.session_state.get("conduite_tests", []), ["Parcours", "Temps (s)", "Niveau"])
    afficher_section("⚽ Remate", st.session_state.get("tests_remate", []), ["Précision Droit (%)", "Précision Gauche (%)", "Vitesse Moy. Droit (km/h)", "Vitesse Moy. Gauche (km/h)"])
    afficher_section("🏃‍♂️ Sprint", st.session_state.get("sprint_tests", []), ["type", "temps", "niveau", "note"])
    afficher_section("🚀 Agilité", st.session_state.get("agility_tests", []), ["Pression", "Temps moyen", "Touches"])
    afficher_section("💪 Masse musculaire", st.session_state.get("muscle_tests", []), ["poids", "masse_musculaire", "niveau", "note"])

    st.markdown("### 🧠 Synthèse IA")
    prompt_global = f"""
Tu es un analyste de performance pour jeunes joueurs de football.

Fais un résumé global de la performance de {nom}, {age} ans, à partir de ses tests techniques et physiques dans les domaines suivants : passe, conduite, remate, sprint, agilité, masse musculaire.

Donne :
1. Une évaluation globale (Excellent / Bon / Moyen / À améliorer)
2. Les points forts
3. Les axes de progression
4. Un plan d’action général sur 4 semaines

Sois concis, professionnel et motivant.
"""
    if st.button("🧠 Générer l'analyse globale IA"):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un préparateur de football jeunesse."},
                    {"role": "user", "content": prompt_global}
                ],
                temperature=0.7,
                max_tokens=600
            )
            st.success("✅ Rapport généré avec succès.")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
