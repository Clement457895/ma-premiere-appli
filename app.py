# =========================================================
# -------------------- IMPORTS ----------------------------
# =========================================================
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# -------------------- TITRE ------------------------------
# =========================================================
st.title("🫁 Cohérence cardiaque")


# =========================================================
# -------------------- ONGLETS ----------------------------
# =========================================================
tab_respiration, tab_parametres = st.tabs(
    ["🌬️ Respiration", "⚙️ Paramètres"]
)


# =========================================================
# -------------------- PARAMÈTRES -------------------------
# =========================================================
with tab_parametres:
    st.header("⚙️ Réglages")

    # =====================================================
    # -------------------- TEMPS --------------------------
    # =====================================================
    inspire = st.number_input("Inspiration (secondes)", 1, 10, 4)
    retenue = st.number_input("Rétention (secondes)", 0, 10, 2)
    expire = st.number_input("Expiration (secondes)", 1, 10, 6)

    # =====================================================
    # -------------------- APPARENCE ----------------------
    # =====================================================
    taille = st.slider("Taille du rond", 100, 220, 150)
    couleur = st.color_picker("Couleur du rond", "#00AAFF")

    # =====================================================
    # -------------------- DURÉE --------------------------
    # =====================================================
    duree_totale = st.number_input("Durée (minutes)", 1, 60, 5)

    # =====================================================
    # -------------------- AUDIO --------------------------
    # =====================================================
    audio_on = st.checkbox("🔊 Activer les sons MP3", True)

    # =====================================================
    # -------------------- CYCLES -------------------------
    # =====================================================
    cycles = int(duree_totale * 60 // (inspire + retenue + expire))


# =========================================================
# -------------------- RESPIRATION ------------------------
# =========================================================
with tab_respiration:

    html_code = f"""
    <style>
    /* ================================================= */
    /* -------------------- ZONE ------------------------ */
    /* ================================================= */
    #zone {{
        height: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    /* ================================================= */
    /* -------------------- CERCLE ---------------------- */
    /* ================================================= */
    #cercle {{
        width: {taille}px;
        height: {taille}px;
        background: {couleur};
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 32px;
        color: white;
        transform-origin: center;
    }}

    #phase {{
        transition: opacity 0.3s;
    }}

    /* ================================================= */
    /* -------------------- CONTROLES ------------------- */
    /* ================================================= */
    .controls {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }}

    button {{
        font-size: 26px;
        padding: 10px 18px;
    }}
    </style>

    <!-- ================================================= -->
    <!-- -------------------- AUDIO ---------------------- -->
    <!-- ================================================= -->
    <audio id="snd-inspire" src="sounds/inspire%20(Roxanne).mp3"></audio>
    <audio id="snd-retiens" src="sounds/retiens%20(Roxanne).mp3"></audio>
    <audio id="snd-expire" src="sounds/expire%20(Roxanne).mp3"></audio>

    <!-- ================================================= -->
    <!-- -------------------- VISUEL --------------------- -->
    <!-- ================================================= -->
    <div id="zone">
        <div id="cercle">
            <span id="phase">Prêt</span>
        </div>
    </div>

    <!-- ================================================= -->
    <!-- -------------------- CONTROLES ------------------ -->
    <!-- ================================================= -->
    <div class="controls">
        <button onclick="playPause()">⏯️</button>
        <button onclick="stop()">⏹️</button>
    </div>

    <script>
    // =================================================
    // -------------------- VARIABLES -------------------
    // =================================================
    const inspire = {inspire} * 1000;
    const retenue = {retenue} * 1000;
    const expire = {expire} * 1000;
    const cyclesMax = {cycles};
    const audioOn = {str(audio_on).lower()};

    const cercle = document.getElementById("cercle");
    const phaseText = document.getElementById("phase");

    const sounds = {{
        inspire: document.getElementById("snd-inspire"),
        retenue: document.getElementById("snd-retiens"),
        expire: document.getElementById("snd-expire"),
    }};

    let running = false;
    let phase = "inspire";
    let cycle = 0;
    let startTime = null;

    // =================================================
    // -------------------- AUDIO -----------------------
    // =================================================
    function playSound(name) {{
        if (!audioOn) return;
        Object.values(sounds).forEach(s => s.pause());
        sounds[name].currentTime = 0;
        sounds[name].play();
    }}

    // =================================================
    // -------------------- TEXTE -----------------------
    // =================================================
    function setPhase(text, sound=null) {{
        phaseText.innerText = text;
        if (sound) playSound(sound);
    }}

    // =================================================
    // -------------------- ANIMATION -------------------
    // =================================================
    function animate(timestamp) {{
        if (!running) {{
            requestAnimationFrame(animate);
            return;
        }}

        if (!startTime) startTime = timestamp;

        const duration =
            phase === "inspire" ? inspire :
            phase === "retenue" ? retenue :
            expire;

        const progress = Math.min((timestamp - startTime) / duration, 1);

        let scale =
            phase === "inspire" ? 1 + 0.4 * progress :
            phase === "expire" ? 1.4 - 0.4 * progress :
            1.4;

        cercle.style.transform = `scale(${scale})`;

        if (progress >= 1) {{
            startTime = timestamp;

            if (phase === "inspire") {{
                phase = retenue > 0 ? "retenue" : "expire";
                setPhase(phase === "retenue" ? "Retiens" : "Expire", phase);
            }}
            else if (phase === "retenue") {{
                phase = "expire";
                setPhase("Expire", "expire");
            }}
            else {{
                cycle++;
                if (cycle >= cyclesMax) {{
                    running = false;
                    setPhase("Terminé");
                    return;
                }}
                phase = "inspire";
                setPhase("Inspire", "inspire");
            }}
        }}

        requestAnimationFrame(animate);
    }}

    // =================================================
    // -------------------- CONTROLES -------------------
    // =================================================
    function playPause() {{
        running = !running;
        if (running && !startTime) {{
            setPhase("Inspire", "inspire");
        }}
    }}

    function stop() {{
        running = false;
        phase = "inspire";
        cycle = 0;
        startTime = null;
        cercle.style.transform = "scale(1)";
        setPhase("Prêt");
    }}

    // =================================================
    // -------------------- INIT ------------------------
    // =================================================
    requestAnimationFrame(animate);
    </script>
    """

    components.html(html_code, height=520)
