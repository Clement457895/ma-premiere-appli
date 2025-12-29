import streamlit as st
import time

st.title("Cohérence cardiaque")

# Onglets
onglet1, onglet2 = st.tabs(["Respiration", "Paramètres"])

# Onglet Respiration
with onglet1:
    st.header("Exercice de respiration")

    inspire = st.number_input("Temps d'inspiration (secondes)", min_value=1, max_value=10, value=4)
    retenue = st.number_input("Temps de rétention (secondes)", min_value=0, max_value=10, value=2)
    expire = st.number_input("Temps d'expiration (secondes)", min_value=1, max_value=10, value=6)
with onglet1:
    st.header("Exercice de respiration")

    # Temps de répétition
    duree_totale = st.number_input("Durée totale (minutes)", min_value=1, max_value=60, value=5)

    # Calcul nombre de cycles
    cycles = int(duree_totale * 60 // (inspire + retenue + expire))

    # Rond centré + texte
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
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        color: white;
        animation: respiration {inspire + retenue + expire}s infinite ease-in-out;
    }}
    </style>
    <div class="cercle">Prêt ?</div>
    """
    st.markdown(animation_html, unsafe_allow_html=True)

    if st.button("Démarrer"):
        for _ in range(cycles):
            st.markdown(f"<div class='cercle' style='background-color:{couleur};'>Inspire</div>", unsafe_allow_html=True)
            time.sleep(inspire)
            if retenue > 0:
                st.markdown(f"<div class='cercle' style='background-color:{couleur};'>Retiens</div>", unsafe_allow_html=True)
                time.sleep(retenue)
            st.markdown(f"<div class='cercle' style='background-color:{couleur};'>Expire</div>", unsafe_allow_html=True)
            time.sleep(expire)
        st.markdown(f"<div class='cercle' style='background-color:{couleur};'>Cycle terminé</div>", unsafe_allow_html=True)


    # Bouton
    if st.button("Démarrer"):
        st.write("Inspire")
        time.sleep(inspire)
        if retenue > 0:
            st.write("Retiens")
            time.sleep(retenue)
        st.write("Expire")
        time.sleep(expire)
        st.write("Cycle terminé")

# Onglet Paramètres
with onglet2:
    st.header("Paramètres avancés")
    st.write("Image de fond, musique, voix (plus tard).")

    taille = st.slider("Taille du rond", min_value=50, max_value=300, value=150)
    couleur = st.color_picker("Couleur du rond", "#00AAFF")

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
