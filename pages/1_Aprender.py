import streamlit as st
import pandas as pd
import utils as utils
import json
st.title("📚 Aprender Kanjis")

# 🧠 nivel seleccionado
level = st.session_state.get("level", "N5")


data = utils.load_kanji_data()

# 🎯 filtrar por nivel
data = data[data["level"] == level]

progress = utils.load_data()

# 🧠 estado
if "index" not in st.session_state:
    st.session_state.index = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ❌ si no hay datos
if len(data) == 0:
    st.warning("No hay kanjis para este nivel")
    st.stop()

# 🔍 filtrar no aprendidos
unlearned = data[~data["kanji"].isin(progress["known"])]

# 🎉 si completado
if len(unlearned) == 0:
    st.success("🎉 Has aprendido todos los kanjis de este nivel")

    if st.button("🔄 Reiniciar nivel"):
        progress["known"] = []
        utils.save_data(progress)
        st.rerun()

    st.stop()

# 🧭 índice seguro
st.session_state.index = st.session_state.index % len(unlearned)
kanji = unlearned.iloc[st.session_state.index]

# 🀄 card
st.markdown(f"""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-bottom: 20px;
">
    <div style="
        font-size: 70px;
        text-align: center;
    ">
        {kanji["kanji"]}
    </div>
</div>
""", unsafe_allow_html=True)

# 🔘 botón
button_text = "👀 Mostrar" if not st.session_state.show_answer else "🙈 Ocultar"

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button(button_text, use_container_width=True):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()

# 📖 resultado
if st.session_state.show_answer:
    st.markdown(f"""
    <div style="
        text-align: center;
        font-size: 22px;
        margin-top: 10px;
        line-height: 1.8;
    ">
    <b>On:</b> {", ".join(kanji["reading_on"])} <br>
    <b>Kun:</b> {", ".join(kanji["reading_kun"])}<br>
    <b>Significado:</b> {kanji["meaning"]}
</div>
    """, unsafe_allow_html=True)

# 🎮 acciones
col1, col2, col3 = st.columns([1,2,1])

with col2:
    colA, colB = st.columns(2)

    with colA:
        if st.button("✔️ Aprendido", use_container_width=True):
            if kanji["kanji"] not in progress["known"]:
                progress["known"].append(kanji["kanji"])
                utils.save_data(progress)

            st.session_state.index += 1
            st.session_state.show_answer = False
            st.rerun()

    with colB:
        if st.button("➡️ Siguiente", use_container_width=True):
            st.session_state.index += 1
            st.session_state.show_answer = False
            st.rerun()

# 📊 progreso
st.divider()

total = len(data)
done = len(progress["known"])

st.progress(done / total if total > 0 else 0)
st.write(f"{done} / {total} kanjis")