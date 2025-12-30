# ---------- IMPORTS ----------
import streamlit as st
import streamlit.components.v1 as components

# ---------- TITRE ----------
st.title("Cohérence cardiaque")

# ---------- ONGLET ----------
onglet_respiration, onglet_parametres = st.tabs(
    ["🫁 Respiration", "⚙️ Paramètres"]
)

# =========================================================
# ---------- PARAMÈTRES ----------
# =========================================================
with onglet_parametres:
    st.header("Paramètres")

    # ---------- TEMPS ----------
    inspire = st.number_input(
        "Temps d'inspiration (secondes)",
        min_value=1, max_value=10, value=4
    )
    retenue = st.number_input(
        "Temps de rétention (secondes)",
        min_value=0, max_value=10, value=2
    )
    expire = st.number_input(
        "Temps d'expiration (secondes)",
        min_value=1, max_value=10, value=6
    )

    # ---------- APPARENCE ----------
    taille = st.slider(
        "Taille du rond",
        min_value=80, max_value=300, value=150
    )
    couleur = st.color_picker(
        "Couleur du rond",
        "#00AAFF"
    )

    # ---------- DURÉE ----------
    duree_totale = st.number_input(
        "Durée totale (minutes)",
        min_value=1, max_value=60, value=5
    )

    # ---------- OPTION VOIX ----------
    voix = st.checkbox("Voix", value=True)

    # ---------- CYCLES ----------
    cycles = int(duree_totale * 60 // (inspire + retenue + expire))

# =========================================================
# ---------- RESPIRATION ----------
# =========================================================
with onglet_respiration:
    st.header("Exercice")

    # ---------- BOUTON ----------
    start = st.button("▶️ Démarrer")

    if start:
        # ---------- HTML / CSS / JS ----------
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
            font-size: 32px;
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
        // ---------- VARIABLES ----------
        const cercle = document.getElementById("cercle");
        const phaseText = document.getElementById("phase");

        const inspire = {inspire} * 1000;
        const retenue = {retenue} * 1000;
        const expire = {expire} * 1000;
        const cycles = {cycles};
        const voix = {str(voix).lower()};

        let cycle = 0;
        let phase = "inspire";
        let startTime = null;
        let startScale = 1;
        let endScale = 1.4;

        // ---------- EASING ----------
        function easeInOutSine(t) {{
            return -(Math.cos(Math.PI * t) - 1) / 2;
        }}

        // -------------------- VOIX (douce et française) --------------------
        function speak(text) {
            if (!voix) return;
        
            const utterance = new SpeechSynthesisUtterance(text);
        
            const voices = speechSynthesis.getVoices();
            const frenchVoice = voices.find(v =>
                v.lang.startsWith("fr") && !v.name.toLowerCase().includes("robot")
            );
        
            if (frenchVoice) {
                utterance.voice = frenchVoice;
            }
        
            utterance.rate = 0.8;   // plus lent
            utterance.pitch = 0.9;  // plus grave
            utterance.volume = 1;
        
            speechSynthesis.cancel();
            speechSynthesis.speak(utterance);
        }
                
        // -------------------- AFFICHAGE TEXTE + VOIX --------------------
        function showPhase(text) {
            phaseText.style.opacity = 0;
            speechSynthesis.getVoices();
        
            setTimeout(() => {
                phaseText.innerText = text;
                phaseText.style.opacity = 1;
        
                // ---- voix uniquement si autorisée ----
                if (voix && text !== "Cycle terminé") {
                    speak(text);
                }
        
            }, 200);
        }

        // ---------- ANIMATION ----------
        function animate(timestamp) {{
            if (!startTime) startTime = timestamp;

            const duration =
                phase === "inspire" ? inspire :
                phase === "retenue" ? retenue :
                expire;

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
                    if (retenue > 0) showPhase("Retiens");
                }}
                else if (phase === "retenue") {{
                    phase = "expire";
                    startScale = 1.4;
                    endScale = 1;
                    showPhase("Expire");
                }}
                else {{
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

        // ---------- DÉMARRAGE ----------
        setTimeout(() => {{
            showPhase("Inspire");
            requestAnimationFrame(animate);
        }}, 200);
        </script>
        """

        components.html(html_code, height=520)
