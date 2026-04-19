import streamlit as st
import random
from utils import load_kanji_data, load_data, save_data, register_answer, get_accuracy

st.title("🧠 Quiz")

# 🧠 nivel
level = st.session_state.get("level", "N5")

# 📊 datos
data = load_kanji_data()
data = data[data["level"] == level]

# 📥 progreso
progress = load_data()

# 🧠 estado inicial
if "current_kanji" not in st.session_state:
    st.session_state.current_kanji = data.sample(1).iloc[0]

if "quiz_options" not in st.session_state:
    st.session_state.quiz_options = []

if "answered" not in st.session_state:
    st.session_state.answered = False

if "user_answer" not in st.session_state:
    st.session_state.user_answer = None


kanji = st.session_state.current_kanji

# 🎯 generar opciones
if not st.session_state.quiz_options:
    all_meanings = list(data["meaning"])
    wrong = [m for m in all_meanings if m != kanji["meaning"]]
    wrong = random.sample(wrong, min(3, len(wrong)))

    st.session_state.quiz_options = wrong + [kanji["meaning"]]
    random.shuffle(st.session_state.quiz_options)

# 🀄 kanji
st.markdown(f"""
<div style="text-align:center; font-size:80px;">
    {kanji["kanji"]}
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center;'>¿Qué significa?</div>", unsafe_allow_html=True)

# 🎯 botones respuesta SOLO si no ha respondido
if not st.session_state.answered:
    for opt in st.session_state.quiz_options:
        if st.button(opt, use_container_width=True):
            st.session_state.user_answer = opt
            st.session_state.answered = True
            st.rerun()

# 📊 si respondió
if st.session_state.answered:
    correct = st.session_state.user_answer == kanji["meaning"]

    progress = register_answer(progress, kanji["kanji"], correct)
    save_data(progress)

    if correct:
        st.success("✅ Correcto")
    else:
        st.error("❌ Incorrecto")
        st.write("Respuesta correcta:", kanji["meaning"])

    st.write("On:", ", ".join(kanji["reading_on"]))
    st.write("Kun:", ", ".join(kanji["reading_kun"]))

    if st.button("➡️ Siguiente"):
        st.session_state.current_kanji = data.sample(1).iloc[0]
        st.session_state.quiz_options = []
        st.session_state.answered = False
        st.session_state.user_answer = None
        st.rerun()


# 📊 estadísticas globales
st.divider()

acc = get_accuracy(progress)

st.metric("📊 Precisión total", f"{acc*100:.1f}%")