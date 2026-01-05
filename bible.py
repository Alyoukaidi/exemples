import streamlit as st
import google.generativeai as genai
import re
import os

# Configuration de la page
st.set_page_config(page_title="Gemini Bible Generator 2026", page_icon="📖")

st.title("📖 Générateur de Bible de Travail")
st.subheader("Analyse factuelle et correction de sous-titres")

# Sidebar pour la configuration
with st.sidebar:
    api_key = st.text_input("Clé API Gemini", type="password")
    st.info("Note : Nous sommes le 05/01/2026. Sébastien Lecornu est Premier Ministre.")

def clean_srt_content(content):
    """Nettoie le contenu du texte SRT directement depuis la mémoire."""
    text_only = re.sub(r'\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n', '', content)
    return os.linesep.join([line for line in text_only.splitlines() if line.strip()])

# Interface de téléchargement
uploaded_file = st.file_uploader("Choisissez un fichier SRT", type="srt")

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    
    if st.button("Générer la Bible"):
        with st.spinner("Analyse et recherche Google en cours..."):
            try:
                # Lecture du fichier
                raw_content = uploaded_file.read().decode("utf-8")
                transcript = clean_srt_content(raw_content)

                # Configuration du modèle avec recherche Google
                model = genai.GenerativeModel(
                    model_name='gemini-2.0-flash',
                    tools=[{"google_search": {}}]
                )

                prompt = f"""
                CONTEXTE : 05/01/2026. Premier Ministre : Sébastien Lecornu.
                Tu es un expert en fact-checking.
                
                MISSION : Analyse ce texte et génère une Bible HTML.
                1. Utilise GOOGLE SEARCH pour valider les noms (ex: Richard Werly).
                2. Applique la nomenclature Larousse.
                3. Crée un tableau HTML avec les corrections et justifications.
                
                TRANSCRIPTION :
                {transcript}
                """

                response = model.generate_content(prompt)
                html_output = response.text

                # Affichage du résultat
                st.success("Analyse terminée !")
                
                # Aperçu du HTML (optionnel)
                with st.expander("Aperçu du code généré"):
                    st.code(html_output, language="html")

                # Bouton de téléchargement
                st.download_button(
                    label="Télécharger la Bible HTML",
                    data=html_output,
                    file_name="BIBLE_TRAVAIL.html",
                    mime="text/html"
                )
                
            except Exception as e:
                st.error(f"Erreur : {e}")
elif not api_key:
    st.warning("Veuillez entrer votre clé API dans la barre latérale.")
