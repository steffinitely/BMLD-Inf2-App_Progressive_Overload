import streamlit as st
from functions.progression import calculate_progression, calculate_training_volume, get_last_entry

st.title("🏋️ Lat Pulldown")

st.markdown("""
Lat Pulldown ist eine ausgezeichnete Rückenübung zur Stärkung des breiten Rückenmuskels.

**Muskeln:**
- Latissimus Dorsi (breiter Rückenmuskel) - Hauptmuskel
- Hintere Schultern
- Bizeps
""")

st.divider()

st.subheader("📊 Deine Fortschritte")

# Placeholder für Daten
st.info("Hier werden deine letzten Trainings angezeigt...")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Neues Training", use_container_width=True):
        st.switch_page("views/upper_exercise_selection.py")
with col2:
    if st.button("← Zurück", use_container_width=True):
        st.switch_page("views/upper_exercise_selection.py")