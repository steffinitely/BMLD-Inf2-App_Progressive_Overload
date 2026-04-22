import streamlit as st

st.title("🏋️ Wähle deinen Split")

st.markdown("""
Trainierst du heute Ober- oder Unterkörper?
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("💪 Oberkörper Übungen", use_container_width=True):
        st.switch_page("views/upper_exercise_selection.py")

with col2:
    if st.button("🦵 Unterkörper Übungen", use_container_width=True):
        st.switch_page("views/lower_exercise_selection.py")

st.divider()

if st.button("← Zurück zur Startseite", use_container_width=True):
    st.switch_page("views/homepage.py")
