import streamlit as st
import streamlit.components.v1 as components
import time

# ---- Titre de l'application ----
st.title("Cohérence cardiaque")

# ---- Onglets ----
onglet1, onglet2 = st.tabs(["Respiration", "Paramètres"])

# -------------------- Onglet Paramètres --------------------
with onglet2:
    st.header("Paramètres avancés")
    
    # Paramètres de respiration
    inspire = st.number_input("Temps d'inspiration (secondes)", min_value=1, max_value=10, value=4, key="inspire")
    retenue = st.number_input("Temps de rétention (secondes)", min_value=0, max_value=10, value=2, key="retenue")
    expire = st.number_input("Temps d'expiration (secondes)", min_value=1, max_value=10, value=6, key="expire")

    # Paramètres du cercle
    taille = st.slider("Taille du rond", min_value=50, max_value=300, value=150, key="taille")
    couleur = st.color_picker("Couleur du rond", "#00AAFF", key="couleur")

    # Durée totale
    duree_totale = st.number_input("Durée totale (minutes)", min_value=1, max_value=60, value=5, key="duree")
    
    # Calcul nombre de cycles
    cycles = int(duree_totale * 60 // (inspire + retenue + expire))

    # --- Option voix ---
    voix = st.checkbox("Voix", value=True, key="voix")

# -------------------- Onglet Respiration --------------------
with onglet1:
    st.header("Exercice de respiration")

    # ---- Bouton démarrer ----
    start = st.button("▶️ Démarrer")
    cont = st.empty()

    if start:
        # ---- HTML + CSS + JS ----
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
            transform-origin: center;
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
        // ---- Variables JS ----
        const cercle = document.getElementById("cercle");
        const phaseText = document.getElementById("phase");
        const inspire = {inspire} * 1000;
        const retenue = {retenue} * 1000;
        const expire = {expire} * 1000;
        const cycles = {cycles};
        const voix = {str(voix).lower()};  // true ou false

        let cycle = 0;
        let phase = "inspire";
        let startTime = null;
        let startScale = 1;
        let endScale = 1.4;

        // ---- Fonction easing ----
        function easeInOutSine(t) {{
            return -(Math.cos(Math.PI * t) - 1)/2;
        }}

        // ---- Affichage du texte ----
        function showPhase(text) {{
            phaseText.style.opacity = 0;
            setTimeout(() => {{
                phaseText.innerText = text;
                phaseText.style.opacity = 1;
                // ---- Voix ----
                if (voix && text !== "Cycle terminé") {{
                    const utterance = new SpeechSynthesisUtterance(text);
                    speechSynthesis.speak(utterance);
                }}
            }}, 200);
        }}

        // ---- Animation du cercle ----
        function animate(timestamp) {{
            if (!startTime) startTime = timestamp;
            const duration = phase === "inspire" ? inspire : phase === "retenue" ? retenue : expire;
            const elapsed = timestamp - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased = easeInOutSine(progress);
            const scale = startScale + (endScale - startScale) * eased;
            cercle.style.transform = "scale(" + scale + ")";

            if (progress >= 1) {{
                if (phase === "inspire") {{
                    phase = "retenue";
                    startScale = 1.4;
                    endScale = 1.4;
                    if(retenue>0) showPhase("Retiens");
                }} else if (phase === "retenue") {{
                    phase = "expire";
                    startScale = 1.4;
                    endScale = 1;
                    showPhase("Expire");
                }} else {{
                    cycle++;
                    if (cycle >= cycles) {{
                        showPhase("Cycle terminé");
                        return;
                    }}
                    phase = "inspire";
                    startScale = 1;
                    endScale = 1.4;
                    showPhase("Inspire");
                }}
                startTime = timestamp;
            }}
            requestAnimationFrame(animate);
        }}

        // ---- Lancer l'animation ----
        setTimeout(() => {{
            showPhase("Inspire");
            requestAnimationFrame(animate);
        }}, 100);
        </script>
        """
       # ---- Affichage ----
        components.html(html_code, height=500)
