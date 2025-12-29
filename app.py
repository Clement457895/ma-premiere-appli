import streamlit as st
import time

st.title("Cohérence cardiaque")

# Onglets
onglet1, onglet2 = st.tabs(["Respiration", "Paramètres"])

# -------------------- Onglet Paramètres --------------------
with onglet2:
    st.header("Paramètres avancés")
    
    # Paramètres du rond et temps
    inspire = st.number_input("Temps d'inspiration (secondes)", min_value=1, max_value=10, value=4, key="inspire")
    retenue = st.number_input("Temps de rétention (secondes)", min_value=0, max_value=10, value=2, key="retenue")
    expire = st.number_input("Temps d'expiration (secondes)", min_value=1, max_value=10, value=6, key="expire")
    taille = st.slider("Taille du rond", min_value=50, max_value=300, value=150, key="taille")
    couleur = st.color_picker("Couleur du rond", "#00AAFF", key="couleur")
    duree_totale = st.number_input("Durée totale (minutes)", min_value=1, max_value=60, value=5, key="duree")
    
    # Calcul nombre de cycles
    cycles = int(duree_totale * 60 // (inspire + retenue + expire))

    # Rond initial + texte centré
    st.markdown(f"""
    <style>
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
    }}
    </style>
    <div class="cercle">Prêt ?</div>
    """, unsafe_allow_html=True)


# -------------------- Onglet Respiration --------------------
with onglet1:
    st.header("Exercice de respiration")

    # Bouton Démarrer
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

# -------------------- Onglet Paramètres --------------------
with onglet2:
    st.header("Paramètres avancés")
    st.write("Ici on mettra plus tard image de fond, musique et voix.")
