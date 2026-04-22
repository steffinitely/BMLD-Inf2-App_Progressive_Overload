import streamlit as st

st.title("🦵 Unterkörper Übungen")

st.markdown("""
Wähle eine Unterkörper Übung zum Trainieren und Trackieren.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🏋️ Barbell Squat", use_container_width=True):
        st.switch_page("views/barbell_squat.py")
    if st.button("🏋️ Barbell Deadlift", use_container_width=True):
        st.switch_page("views/barbell_deadlift.py")

with col2:
    if st.button("🏋️ Dumbbell Bulgarian Split Squat", use_container_width=True):
        st.switch_page("views/dumbbell_bulgariansquat.py")

st.divider()

if st.button("← Zurück zum Split", use_container_width=True):
    st.switch_page("views/workout_selection.py")
