import streamlit as st

st.title("Cohérence cardiaque")

onglet1, onglet2 = st.tabs(["Respiration", "Paramètres"])

with onglet1:
    st.header("Exercice de respiration")
    start = st.button("▶️ Démarrer")

    if start:
        st.success("Le bouton fonctionne 🎉")

with onglet2:
    st.write("Paramètres")
