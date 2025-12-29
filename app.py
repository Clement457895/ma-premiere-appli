import streamlit as st
import time

st.title("Cohérence cardiaque")

# Création des onglets
onglet1, onglet2 = st.tabs(["Respiration", "Paramètres"])

# Onglet 1 : Exercice de respiration
with onglet1:
    st.header("Exercice de respiration")

    # Paramètres de temps
    inspire = st.number_input(
        "Temps d'inspiration (secondes)",
        min_value=1,
        max_value=10,
        value=4
    )

    retenue = st.number_input(
        "Temps de rétention (secondes)",
        min_value=0,
        max_value=10,
        value=2
    )

    expire = st.number_input(
        "Temps d'expiration (secondes)",
        min_value=1,
        max_value=10,
        value=6
    )

    # Paramètres visuels du rond
    taille = st.slider(
        "Taille du rond",
        min_value=50,
        max_value=300,
        value=150
    )

    couleur = st.color_picker(
        "Couleur du rond",
        "#00AAFF"
    )

    # Rond animé
    animation_html = f"""
    <style>
    @keyframes respiration {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.4); }}
        100% {{ transform: scale(1); }}
    }}
    .cercle {{
        width: {taille}px;
        height: {taille}px;
        background-color: {couleur};
        border-radius: 50%;
        margin: 40px auto;
        animation: respiration {inspire + retenue + expire}s infinite ease-in-out;
    }}
    </style>
    <div class="cercle"></div>
    """
    st.markdown(animation_html, unsafe_allow_html=True)

    # Bouton Démarrer
    if st.button("Démarrer"):
        st.write("Inspire")
        time.sleep(inspire)
        if retenue > 0:
            st.write("Retiens")
            time.sleep(retenue)
        st.write("Expire")
        time.sleep(expire)
        st.write("Cycle terminé")

# Onglet 2 : Paramètres avancés
with onglet2:
    st.header("Paramètres avancés")
    st.write("Image de fond, musique, voix (plus tard).")
