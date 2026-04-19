import streamlit as st
import pandas as pd
import json

data = pd.DataFrame([
    {"kanji": "日", "meaning": "sol / día", "reading": "にち / ひ"},
    {"kanji": "月", "meaning": "luna / mes", "reading": "げつ / つき"},
    {"kanji": "水", "meaning": "agua", "reading": "すい / みず"},
])

FILE = "data.json"

def load_data():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"known": []}

def save_data(data_json):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=2)

# estado
if "index" not in st.session_state:
    st.session_state.index = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

progress = load_data()

unlearned = data[~data["kanji"].isin(progress["known"])]

# si no quedan kanjis
if len(unlearned) == 0:
    st.success("🎉 ¡Has aprendido todos los kanjis!")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🔄 Reiniciar progreso", use_container_width=True):
            progress["known"] = []
            save_data(progress)
            st.rerun()

    st.stop()

# índice seguro
st.session_state.index = st.session_state.index % len(unlearned)
kanji = unlearned.iloc[st.session_state.index]

st.title("📖 Kanji Journal")

# card
st.markdown(f"""
<div style="
    padding: 25px;
    border-radius: 20px;
    background-color: #ffffff;
    color: #000000;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
">
    <h1 style="font-size:70px;">{kanji["kanji"]}</h1>
</div>
""", unsafe_allow_html=True)

# botón central
button_text = "👀 Mostrar resultado" if not st.session_state.show_answer else "🙈 Ocultar resultado"

col1, col2, col3 = st.columns([1,2,1])
with col2:
    clicked = st.button(button_text, use_container_width=True)

if clicked:
    st.session_state.show_answer = not st.session_state.show_answer
    st.rerun()

# resultado
if st.session_state.show_answer:
    st.markdown(f"""
    <div style="text-align:center; font-size:28px;">
        <div style="font-size:32px;">{kanji["reading"]}</div>
        <div style="opacity:0.7;">{kanji["meaning"]}</div>
    </div>
    """, unsafe_allow_html=True)

# botones abajo centrados
col1, col2, col3 = st.columns([1,2,1])

with col2:
    colA, colB = st.columns(2)

    with colA:
        if st.button("✔️ Aprendido", use_container_width=True):
            if kanji["kanji"] not in progress["known"]:
                progress["known"].append(kanji["kanji"])
                save_data(progress)

            st.session_state.index = (st.session_state.index + 1) % len(unlearned)
            st.session_state.show_answer = False
            st.rerun()

    with colB:
        if st.button("➡️ Siguiente", use_container_width=True):
            st.session_state.index = (st.session_state.index + 1) % len(unlearned)
            st.session_state.show_answer = False
            st.rerun()

# progreso
st.divider()

total = len(data)
done = len(progress["known"])

st.subheader("📊 Progreso")
st.progress(done / total if total > 0 else 0)
st.write(f"{done} / {total} kanjis aprendidos")