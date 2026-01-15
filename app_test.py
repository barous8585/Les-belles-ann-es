import streamlit as st

st.title("🏠 Les Belles Années - Test Déploiement")
st.success("✅ L'application fonctionne !")
st.info("Si vous voyez ce message, le déploiement est OK.")

if st.button("Charger l'app complète"):
    st.write("Redirection vers app.py...")
