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
# -------------------- ONGLET -----------------------------
# =========================================================
onglet_respiration, onglet_parametres = st.tabs(
    ["Respiration", "Paramètres"]
)

# =========================================================
# -------------------- PARAMÈTRES -------------------------
# =========================================================
with onglet_parametres:
    st.header("⚙️ Paramètres")

    # ---------- TEMPS ----------
    inspire = st.number_input("Inspiration (secondes)", 1, 10, 4)
    retenue = st.number_input("Rétention (secondes)", 0, 10, 2)
    expire = st.number_input("Expiration (secondes)", 1, 10, 6)

    # ---------- APPARENCE ----------
    taille = st.slider("Taille du rond", 80, 220, 150)
    couleur = st.color_picker("Couleur du rond", "#00AAFF")

    # ---------- DURÉE ----------
    duree_totale = st.number_input("Durée (minutes)", 1, 60, 5)

    # ---------- AUDIO ----------
    audio_on = st.checkbox("🔊 Sons MP3", value=True)

    # ---------- CYCLES ----------
    cycles = int(duree_totale * 60 // (inspire + retenue + expire))

# =========================================================
# -------------------- RESPIRATION ------------------------
# =========================================================
with onglet_respiration:
    st.header("🌬️ Exercice")

    html_code = f"""
    <style>
    /* ================================================= */
    /* ---------------- ZONE FIXE ---------------------- */
    /* ================================================= */
    #zone {{
        height: 320px;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    /* ================================================= */
    /* ---------------- CERCLE ------------------------- */
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
        opacity: 0;
        transition: opacity 0.4s ease-in-out;
    }}

    /* ================================================= */
    /* ---------------- CONTROLES ---------------------- */
    /* ================================================= */
    .controls {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
        gap: 20px;
    }}

    button {{
        font-size: 24px;
        padding: 10px 20px;
    }}
    </style>

    <!-- ================================================= -->
    <!-- ---------------- AUDIO -------------------------- -->
    <!-- ================================================= -->
    <audio id="snd-inspire" src="sounds/inspire%20(Roxanne).mp3"></audio>
    <audio id="snd-retiens" src="sounds/retiens%20(Roxanne).mp3"></audio>
    <audio id="snd-expire" src="sounds/expire%20(Roxanne).mp3"></audio>

    <!-- ================================================= -->
    <!-- ---------------- VISUEL ------------------------- -->
    <!-- ================================================= -->
    <div id="zone">
        <div id="cercle">
            <span id="phase">Prêt</span>
        </div>
    </div>

    <!-- ================================================= -->
    <!-- ---------------- CONTROLES ----------------------- -->
    <!-- ================================================= -->
    <div class="controls">
        <button onclick="toggle()">⏯️ Pause/Play</button>
        <button onclick="stopAll()">⏹️ Arrêter</button>
    </div>

    <script>
    // =================================================
    // ---------------- VARIABLES ----------------------
    // =================================================
    const inspire = {inspire} * 1000;
    const retenue = {retenue} * 1000;
    const expire = {expire} * 1000;
    const cycles = {cycles};
    const audioOn = {str(audio_on).lower()};

    const cercle = document.getElementById("cercle");
    const phaseText = document.getElementById("phase");

    const sndInspire = document.getElementById("snd-inspire");
    const sndRetiens = document.getElementById("snd-retiens");
    const sndExpire = document.getElementById("snd-expire");

    let running = false;
    let audioUnlocked = false;

    let cycle = 0;
    let phase = "inspire";
    let startTime = null;
    let scaleFrom = 1;
    let scaleTo = 1.4;

    // =================================================
    // ---------------- AUDIO --------------------------
    // =================================================
    function playSound(name) {{
        if (!audioOn || !audioUnlocked) return;

        sndInspire.pause();
        sndRetiens.pause();
        sndExpire.pause();

        if (name === "inspire") {{
            sndInspire.currentTime = 0;
            sndInspire.play();
        }}
        if (name === "retenue") {{
            sndRetiens.currentTime = 0;
            sndRetiens.play();
        }}
        if (name === "expire") {{
            sndExpire.currentTime = 0;
            sndExpire.play();
        }}
    }}

    // =================================================
    // ---------------- TEXTE --------------------------
    // =================================================
    function show(text, sound) {{
        phaseText.style.opacity = 0;
        setTimeout(() => {{
            phaseText.innerText = text;
            phaseText.style.opacity = 1;
            if (sound) playSound(sound);
        }}, 200);
    }}

    // =================================================
    // ---------------- ANIMATION ----------------------
    // =================================================
    function animate(ts) {{
        if (!running) {{
            requestAnimationFrame(animate);
            return;
        }}

        if (!startTime) startTime = ts;

        const duration =
            phase === "inspire" ? inspire :
            phase === "retenue" ? retenue :
            expire;

        const progress = Math.min((ts - startTime) / duration, 1);
        const eased = -(Math.cos(Math.PI * progress) - 1) / 2;

        const scale = scaleFrom + (scaleTo - scaleFrom) * eased;
        cercle.style.transform = "scale(" + scale + ")";

        if (progress >= 1) {{
            if (phase === "inspire") {{
                phase = "retenue";
                scaleFrom = 1.4;
                scaleTo = 1.4;
                if (retenue > 0) show("Retiens", "retenue");
            }}
            else if (phase === "retenue") {{
                phase = "expire";
                scaleFrom = 1.4;
                scaleTo = 1;
                show("Expire", "expire");
            }}
            else {{
                cycle++;
                if (cycle >= cycles) {{
                    show("Terminé", null);
                    running = false;
                    return;
                }}
                phase = "inspire";
                scaleFrom = 1;
                scaleTo = 1.4;
                show("Inspire", "inspire");
            }}
            startTime = ts;
        }}

        requestAnimationFrame(animate);
    }}

    // =================================================
    // ---------------- CONTROLES ----------------------
    // =================================================
    function toggle() {{
        running = !running;

        // 🔓 Débloque le son au premier clic
        if (!audioUnlocked) {{
            audioUnlocked = true;
            show("Inspire", "inspire");
        }}
    }}

    function stopAll() {{
        running = false;
        cercle.style.transform = "scale(1)";
        phaseText.innerText = "Arrêté";
    }}

    // =================================================
    // ---------------- INIT ---------------------------
    // =================================================
    show("Prêt", null);
    requestAnimationFrame(animate);
    </script>
    """

    components.html(html_code, height=520)
