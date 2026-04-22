import streamlit as st

st.title("💪 Oberkörper Übungen")

st.markdown("""
Wähle eine Oberkörper Übung zum Trainieren und Trackieren.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🏋️ Barbell Benchpress", use_container_width=True):
        st.switch_page("views/barbell_benchpress.py")
    if st.button("🏋️ Dumbbell Shoulder Press", use_container_width=True):
        st.switch_page("views/dumbbell_shoulderpress.py")

with col2:
    if st.button("🏋️ Lat Pulldown", use_container_width=True):
        st.switch_page("views/latpulldownmachine.py")

st.divider()

if st.button("← Zurück zum Split", use_container_width=True):
    st.switch_page("views/workout_selection.py")
