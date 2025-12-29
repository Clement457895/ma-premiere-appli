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



# -------------------- Onglet Respiration --------------------
with onglet1:
    st.header("Exercice de respiration")

    start = st.button("▶️ Démarrer")
    total_cycle = inspire + retenue + expire
    cycles = int(duree_totale * 60 // total_cycle)
    cont = st.empty()
    
    if start:
        html_code = f"""
        <div id="cercle" style="
            width:{taille}px;
            height:{taille}px;
            background-color:{couleur};
            border-radius:50%;
            margin:50px auto;
            display:flex;
            justify-content:center;
            align-items:center;
            font-size:30px;
            color:white;
            transition: all 1s linear;
        ">Prêt ?</div>

        <script>
        const cercle = document.getElementById("cercle");
        const inspire = {inspire} * 1000;
        const retenue = {retenue} * 1000;
        const expire = {expire} * 1000;
        const cycles = {cycles};
        const taille = {taille};

        let cycle = 0;

        function runCycle() {{
            if (cycle >= cycles) {{
                cercle.innerText = "Cycle terminé";
                return;
            }}

            cercle.innerText = "Inspire";
            cercle.style.width = (taille * 1.4) + "px";
            cercle.style.height = (taille * 1.4) + "px";

            setTimeout(() => {{
                cercle.innerText = "Retiens";

                setTimeout(() => {{
                    cercle.innerText = "Expire";
                    cercle.style.width = taille + "px";
                    cercle.style.height = taille + "px";

                    setTimeout(() => {{
                        cycle++;
                        runCycle();
                    }}, expire);

                }}, retenue);

            }}, inspire);
        }}

        runCycle();
        </script>
        """

        cont.markdown(html_code, unsafe_allow_html=True)
    
