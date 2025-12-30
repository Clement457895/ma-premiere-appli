import streamlit as st
import streamlit.components.v1 as components
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
    cont = st.empty()

    if start:
        html_code = f"""
        <style>
        #cercle {{
            width: {taille}px;
            height: {taille}px;
            background-color: {couleur};
            border-radius: 50%;
            margin: 50px auto;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 30px;
            color: white;
        }}
        .phase-text {{
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }}
        </style>

        <div id="cercle">
            <span id="phase" class="phase-text">Prêt ?</span>
        </div>

        <script>
        const cercle = document.getElementById("cercle");
        const phaseText = document.getElementById("phase");
        const inspire = {inspire} * 1000;
        const retenue = {retenue} * 1000;
        const expire = {expire} * 1000;
        const cycles = {cycles};
        const taille = {taille};

        let cycle = 0;
        let phase = "inspire"; // inspire, retenue, expire
        let startTime = null;
        let startSize = taille;
        let endSize = taille * 1.4;

        function easeInOutSine(t) {{
            return -(Math.cos(Math.PI * t) - 1)/2;
        }}

        function showPhase(text) {{
            phaseText.style.opacity = 0;
            setTimeout(() => {{
                phaseText.innerText = text;
                phaseText.style.opacity = 1;
            }}, 200);
        }}

        function animate(timestamp) {{
            if (!startTime) startTime = timestamp;
            const duration = phase === "inspire" ? inspire : phase === "retenue" ? retenue : expire;
            const elapsed = timestamp - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = easeInOutSine(progress);
            const size = startSize + (endSize - startSize) * eased;
            cercle.style.width = size + "px";
            cercle.style.height = size + "px";

            if (progress >= 1) {{
                // Changer de phase
                if (phase === "inspire") {{
                    phase = "retenue";
                    startSize = taille*1.4;
                    endSize = taille*1.4;
                    showPhase("Retiens");
                }} else if (phase === "retenue") {{
                    phase = "expire";
                    startSize = taille*1.4;
                    endSize = taille;
                    showPhase("Expire");
                }} else {{
                    cycle++;
                    if (cycle >= cycles) {{
                        showPhase("Cycle terminé");
                        return;
                    }}
                    phase = "inspire";
                    startSize = taille;
                    endSize = taille*1.4;
                    showPhase("Inspire");
                }}
                startTime = timestamp;
            }}

            requestAnimationFrame(animate);
        }}

        setTimeout(() => {{
            showPhase("Inspire");
            requestAnimationFrame(animate);
        }}, 100);
        </script>
        """
        components.html(html_code, height=500)
