# =========================================================
# -------------------- IMPORTS -----------------------------
# =========================================================
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# -------------------- TITRE -------------------------------
# =========================================================
st.set_page_config(page_title="Cohérence cardiaque", layout="centered")
st.title("🫁 Cohérence cardiaque")


# =========================================================
# -------------------- ONGLETS -----------------------------
# =========================================================
onglet_respiration, onglet_parametres = st.tabs(
    ["Respiration", "Paramètres"]
)


# =========================================================
# -------------------- PARAMÈTRES --------------------------
# =========================================================
with onglet_parametres:
    st.header("⚙️ Paramètres")

    # ---------- Temps ----------
    inspire = st.number_input(
        "Inspiration (secondes)", 1, 10, 4
    )
    retenue = st.number_input(
        "Rétention (secondes)", 0, 10, 2
    )
    expire = st.number_input(
        "Expiration (secondes)", 1, 10, 6
    )

    # ---------- Apparence ----------
    taille = st.slider(
        "Taille du rond", 80, 300, 160
    )
    couleur = st.color_picker(
        "Couleur du rond", "#00AAFF"
    )

    # ---------- Durée ----------
    duree = st.number_input(
        "Durée totale (minutes)", 1, 60, 5
    )

    # ---------- Son ----------
    voix = st.checkbox("Son (doux)", value=True)

    # ---------- Cycles ----------
    cycles = int((duree * 60) // (inspire + retenue + expire))


# =========================================================
# -------------------- RESPIRATION -------------------------
# =========================================================
with onglet_respiration:
    st.header("🌬️ Exercice")

    # ---------- HTML / CSS / JS ----------
    html_code = f"""
    <style>
        body {{
            text-align: center;
        }}

        #cercle {{
            width: {taille}px;
            height: {taille}px;
            background: {couleur};
            border-radius: 50%;
            margin: 40px auto;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 32px;
            color: white;
            transform-origin: center;
        }}

        #controls {{
            display: flex;
            justify-content: center;
            gap: 20px;
        }}

        button {{
            font-size: 20px;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
        }}
    </style>

    <div id="cercle">
        <span id="phase">Prêt</span>
    </div>

    <div id="controls">
        <button id="playPause">▶️ Démarrer</button>
        <button id="stop">⏹️ Stop</button>
    </div>

    <script>
    // =====================================================
    // -------------------- VARIABLES -----------------------
    // =====================================================
    const cercle = document.getElementById("cercle");
    const phaseText = document.getElementById("phase");

    const inspire = {inspire} * 1000;
    const retenue = {retenue} * 1000;
    const expire = {expire} * 1000;
    const cycles = {cycles};
    const soundOn = {str(voix).lower()};

    let phase = "inspire";
    let cycle = 0;

    let startTime = null;
    let pausedAt = 0;

    let isRunning = false;
    let isPaused = false;

    let startScale = 1;
    let endScale = 1.4;


    // =====================================================
    // -------------------- EASING --------------------------
    // =====================================================
    function easeInOut(t) {{
        return -(Math.cos(Math.PI * t) - 1) / 2;
    }}


    // =====================================================
    // -------------------- SON DOUX ------------------------
    // =====================================================
    function playTone(freq) {{
        if (!soundOn) return;

        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "sine";
        osc.frequency.value = freq;

        gain.gain.setValueAtTime(0.001, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.2, ctx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start();
        osc.stop(ctx.currentTime + 0.4);
    }}


    // =====================================================
    // -------------------- TEXTE + SON ---------------------
    // =====================================================
    function showPhase(text) {{
        phaseText.innerText = text;

        if (soundOn) {{
            if (text === "Inspire") playTone(220);
            if (text === "Expire") playTone(440);
        }}
    }}


    // =====================================================
    // -------------------- ANIMATION -----------------------
    // =====================================================
    function animate(timestamp) {{
        if (!isRunning || isPaused) return;

        if (!startTime) startTime = timestamp;

        const duration =
            phase === "inspire" ? inspire :
            phase === "retenue" ? retenue :
            expire;

        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeInOut(progress);

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
                    showPhase("Terminé");
                    isRunning = false;
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


    // =====================================================
    // -------------------- BOUTONS -------------------------
    // =====================================================
    const playPauseBtn = document.getElementById("playPause");
    const stopBtn = document.getElementById("stop");

    playPauseBtn.onclick = () => {{
        if (!isRunning) {{
            isRunning = true;
            isPaused = false;
            playPauseBtn.innerText = "⏸️ Pause";
            showPhase("Inspire");
            requestAnimationFrame(animate);
            return;
        }}

        if (!isPaused) {{
            isPaused = true;
            pausedAt = performance.now();
            playPauseBtn.innerText = "▶️ Reprendre";
        }} else {{
            isPaused = false;
            startTime += performance.now() - pausedAt;
            playPauseBtn.innerText = "⏸️ Pause";
            requestAnimationFrame(animate);
        }}
    }};

    stopBtn.onclick = () => {{
        isRunning = false;
        isPaused = false;
        cycle = 0;
        phase = "inspire";
        startTime = null;
        cercle.style.transform = "scale(1)";
        phaseText.innerText = "Arrêté";
        playPauseBtn.innerText = "▶️ Démarrer";
    }};
    </script>
    """

    components.html(html_code, height=520)
