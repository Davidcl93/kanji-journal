import streamlit as st
import pandas as pd
import random
import sys
import os

# 👇 para poder importar utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils import generate_options

st.title("🧠 Quiz de Kanjis")

# 🧠 nivel
level = st.session_state.get("level", "N5")

# 📊 DATA (temporal, luego lo cambiamos por JSON)
data = pd.DataFrame([
    {"kanji": "日", "meaning": "sol / día", "reading": "にち / ひ", "level": "N5"},
    {"kanji": "月", "meaning": "luna / mes", "reading": "げつ / つき", "level": "N5"},
    {"kanji": "水", "meaning": "agua", "reading": "すい / みず", "level": "N5"},
    {"kanji": "火", "meaning": "fuego", "reading": "か / ひ", "level": "N5"},
])

# 🎯 filtrar nivel
data = data[data["level"] == level]

if len(data) == 0:
    st.warning("No hay kanjis para este nivel")
    st.stop()

# 🧠 estado
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "quiz_options" not in st.session_state:
    st.session_state.quiz_options = []

if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None

if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

# 🧭 índice seguro
st.session_state.quiz_index = st.session_state.quiz_index % len(data)
kanji = data.iloc[st.session_state.quiz_index]

# 🎯 generar opciones SOLO si no existen
if not st.session_state.quiz_options:
    st.session_state.quiz_options = generate_options(
        kanji["meaning"], data
    )

# 🀄 mostrar kanji
st.markdown(f"""
<div style="
    text-align:center;
    font-size:70px;
    margin-bottom:20px;
">
    {kanji["kanji"]}
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align:center;'>¿Qué significa?</div>", unsafe_allow_html=True)

# 🔘 opciones
for option in st.session_state.quiz_options:
    if st.button(option, use_container_width=True):
        if not st.session_state.quiz_answered:
            st.session_state.quiz_selected = option
            st.session_state.quiz_answered = True
            st.rerun()

# ✅ feedback
if st.session_state.quiz_answered:
    if st.session_state.quiz_selected == kanji["meaning"]:
        st.success("✅ Correcto!")
    else:
        st.error(f"❌ Incorrecto. Era: {kanji['meaning']}")

    st.markdown(f"""
    <div style="text-align:center; margin-top:10px;">
        📖 {kanji["reading"]}
    </div>
    """, unsafe_allow_html=True)

    # 👉 botón siguiente
    if st.button("➡️ Siguiente"):
        st.session_state.quiz_index += 1
        st.session_state.quiz_options = []
        st.session_state.quiz_selected = None
        st.session_state.quiz_answered = False
        st.rerun()

# 📊 progreso simple
st.divider()
st.write(f"Pregunta {st.session_state.quiz_index + 1} / {len(data)}")