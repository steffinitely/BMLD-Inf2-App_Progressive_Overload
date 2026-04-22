import streamlit as st
from functions.progression import calculate_progression, calculate_training_volume, get_last_entry

st.title("🏋️ Barbell Squat")

st.markdown("""
Barbell Squat ist die König-Übung für Beintraining und Gesamtkörperkraft.

**Muskeln:**
- Quadrizeps - Hauptmuskel
- Hamstrings
- Gesäß (Glutes)
- Unterer Rücken
""")

st.divider()

st.subheader("📊 Deine Fortschritte")

# Placeholder für Daten
st.info("Hier werden deine letzten Trainings angezeigt...")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Neues Training", use_container_width=True):
        st.switch_page("views/lower_exercise_selection.py")
with col2:
    if st.button("← Zurück", use_container_width=True):
        st.switch_page("views/lower_exercise_selection.py")