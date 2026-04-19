import streamlit as st

st.title("📖 Kanji Journal")

level = st.selectbox(
    "Selecciona nivel",
    ["N5", "N4", "N3"]
)

st.session_state.level = level

st.write(f"Nivel actual: {level}")

if st.button("📚 Aprender"):
    st.switch_page("pages/1_📚_Aprender.py")