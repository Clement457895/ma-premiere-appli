# =========================================================
# -------------------- IMPORTS -----------------------------
# =========================================================
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# -------------------- CONFIG ------------------------------
# =========================================================
st.set_page_config(page_title="Cohérence cardiaque", layout="centered")
st.title("🫁 Cohérence cardiaque")


# =========================================================
# -------------------- ONGLET ------------------------------
# =========================================================
tab_exercice, tab_param = st.tabs(["Respiration", "Paramètres"])


# =========================================================
# -------------------- PARAMÈTRES --------------------------
# =========================================================
with tab_param:
    st.header("⚙️ Paramètres")

    # ---------- Temps ----------
    inspire = st.number_input("Inspiration (s)", 1, 10, 4)
    retenue = st.number_input("Rétention (s)", 0, 10, 2)
    expire = st.number_input("Expiration (s)", 1, 10, 6)

    # ---------- Apparence ----------
    taille = st.slider("Taille du rond", 80, 280, 160)
    couleur = st.color_picker("Couleur du rond", "#00AAFF")

    # ---------- Durée ----------
    duree = st.number_input("Durée totale (minutes)", 1, 60, 5)

    # ---------- Audio ----------
    son = st.checkbox("🔔 Son (bip doux)", value=True)
    voix = st.checkbox("🗣️ Voix (Inspire / Retiens / Expire)", value=False)

    # ---------- Cycles ----------
    cycles = int((duree * 60) // (inspire + retenue + expire))


# =========================================================
# -------------------- EXERCICE ----------------------------
# =========================================================
with tab_exercice:
    st.header("🌬️ Exercice")

    html_code = f"""
    <style>
        body {{
            text-align: center;
        }}

        #container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}

        #cercle-wrapper {{
            height: 320px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        #cercle {{
            width: {taille}px;
            height: {taille}px;
            background: {couleur};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            color: white;
            transform-origin: center;
        }}

        #controls {{
            display: flex;
            gap: 20px;
        }}

        button {{
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
        }}
    </style>

    <div id="container">
        <div id="cercle-wrapper">
            <div id="cercle">
                <span id="phase">Prêt</span>
            </div>
        </div>

        <div id="controls">
            <button id="playPause">▶️ Démarrer</button>
            <button id="stop">⏹️ Stop</button>
        </div>
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
    const cyclesMax = {cycles};

    const sonOn = {str(son).lower()};
    const voixOn = {str(voix).lower()};

    let phase = "inspire";
    let cycle = 0;

    let running = false;
    let paused = false;
    let startTime = null;
    let pauseTime = null;

    let startScale = 1;
    let endScale = 1.4;


    // =====================================================
    // -------------------- EASING --------------------------
    // =====================================================
    function ease(t) {{
        return -(Math.cos(Math.PI * t) - 1) / 2;
    }}


    // =====================================================
    // -------------------- SON BIP -------------------------
    // =====================================================
    function bip(freq) {{
        if (!sonOn) return;

        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.frequency.value = freq;
        osc.type = "sine";

        gain.gain.setValueAtTime(0.001, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.2, ctx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start();
        osc.stop(ctx.currentTime + 0.4);
    }}


    // =====================================================
    // -------------------- VOIX ----------------------------
    // =====================================================
    function speak(text) {{
        if (!voixOn) return;

        const u = new SpeechSynthesisUtterance(text);
        u.lang = "fr-FR";
        u.rate = 0.85;
        u.pitch = 0.9;

        speechSynthesis.cancel();
        speechSynthesis.speak(u);
    }}


    // =====================================================
    // -------------------- PHASE ---------------------------
    // =====================================================
    function setPhase(text) {{
        phaseText.innerText = text;

        if (text === "Inspire") {{
            bip(220);
            speak("Inspire");
        }}

        if (text === "Retiens") {{
            speak("Retiens");
        }}

        if (text === "Expire") {{
            bip(440);
            speak("Expire");
        }}
    }}


    // =====================================================
    // -------------------- ANIMATION -----------------------
    // =====================================================
    function animate(ts) {{
        if (!running || paused) return;

        if (!startTime) startTime = ts;

        const duration =
            phase === "inspire" ? inspire :
            phase === "retenue" ? retenue :
            expire;

        const elapsed = ts - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const scale = startScale + (endScale - startScale) * ease(progress);

        cercle.style.transform = "scale(" + scale + ")";

        if (progress >= 1) {{
            if (phase === "inspire") {{
                phase = "retenue";
                startScale = 1.4;
                endScale = 1.4;
                if (retenue > 0) setPhase("Retiens");
            }}
            else if (phase === "retenue") {{
                phase = "expire";
                startScale = 1.4;
                endScale = 1;
                setPhase("Expire");
            }}
            else {{
                cycle++;
                if (cycle >= cyclesMax) {{
                    phaseText.innerText = "Terminé";
                    running = false;
                    return;
                }}
                phase = "inspire";
                startScale = 1;
                endScale = 1.4;
                setPhase("Inspire");
            }}
            startTime = ts;
        }}

        requestAnimationFrame(animate);
    }}


    // =====================================================
    // -------------------- BOUTONS -------------------------
    // =====================================================
    document.getElementById("playPause").onclick = () => {{
        if (!running) {{
            running = true;
            paused = false;
            cycle = 0;
            phase = "inspire";
            startScale = 1;
            endScale = 1.4;
            startTime = null;
            setPhase("Inspire");
            requestAnimationFrame(animate);
            document.getElementById("playPause").innerText = "⏸️ Pause";
            return;
        }}

        paused = !paused;
        document.getElementById("playPause").innerText = paused ? "▶️ Reprendre" : "⏸️ Pause";
        if (!paused) requestAnimationFrame(animate);
    }};

    document.getElementById("stop").onclick = () => {{
        running = false;
        paused = false;
        cycle = 0;
        phaseText.innerText = "Arrêté";
        cercle.style.transform = "scale(1)";
        document.getElementById("playPause").innerText = "▶️ Démarrer";
    }};
    </script>
    """

    components.html(html_code, height=560)
