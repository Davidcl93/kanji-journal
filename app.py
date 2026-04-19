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
    import json
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=2)

# estado
if "index" not in st.session_state:
    st.session_state.index = 0

progress = load_data()
total_kanji = len(data)
known_kanji = len(progress["known"])

progress_percent = (known_kanji / total_kanji) * 100 if total_kanji > 0 else 0
unlearned = data[~data["kanji"].isin(progress["known"])]

# 🚨 PRIMERO: check de vacío
if len(unlearned) == 0:
    st.success("🎉 ¡Has aprendido todos los kanjis!")

    if st.button("🔄 Reiniciar progreso"):
        progress["known"] = []
        save_data(progress)
        st.rerun()

    st.stop()

# ✅ SOLO si hay datos seguimos aquí
st.session_state.index = st.session_state.index % len(unlearned)
kanji = unlearned.iloc[st.session_state.index]




st.title("📖 Kanji Journal")

st.markdown(f"""
<div style="
    padding: 20px;
    border-radius: 15px;
    background-color: #f7f7f9;
    text-align: center;
    margin-bottom: 10px;
">
    <h1 style="font-size:60px">{kanji["kanji"]}</h1>
    <h3>{kanji["meaning"]}</h3>
</div>
""", unsafe_allow_html=True)
st.subheader(kanji["meaning"])

if st.button("Mostrar lectura"):
    st.write(kanji["reading"])


col1, col2 = st.columns(2)

with col1:
    if st.button("✔️ Lo he aprendido"):
        if kanji["kanji"] not in progress["known"]:
            progress["known"].append(kanji["kanji"])
            save_data(progress)
            st.success("Guardado ✔️")

        # avanzar automáticamente
        st.session_state.index = (st.session_state.index + 1) % len(unlearned)
        st.rerun()

with col2:
    if st.button("➡️ Siguiente"):
        st.session_state.index = (st.session_state.index + 1) % len(data)
        st.rerun()

st.divider()

st.write(f"Kanjis aprendidos: {len(progress['known'])}")
total = len(data)
done = len(progress["known"])

st.subheader("📊 Progreso")

st.progress(done / total if total > 0 else 0)

st.write(f"{done} / {total} kanjis")