import streamlit as st
from functions.progression import calculate_progression, calculate_training_volume, get_last_entry

if "training_mode" not in st.session_state:
    st.session_state.training_mode = False

st.title("🏋️ Barbell Benchpress")

st.markdown("""
Barbell Benchpress ist eine fundamentale Oberkörper-Übung zur Stärkung von Brust, Schultern und Trizeps.

**Muskeln:**
- Brust (Hauptmuskel)
- Schultern (vordere Deltamuskeln)
- Trizeps
""")

st.divider()

if not st.session_state.training_mode:
    st.subheader("📊 Deine Fortschritte")
    st.info("Hier werden deine letzten Trainings angezeigt...")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Neues Training", use_container_width=True):
            st.session_state.training_mode = True
            st.rerun()
    with col2:
        if st.button("← Zurück", use_container_width=True):
            st.switch_page("views/upper_exercise_selection.py")
else:
    st.subheader("➕ Neues Training erfassen")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Gewicht (kg)", min_value=0.0, step=0.5, format="%.1f")
    with col2:
        reps = st.number_input("Wiederholungen", min_value=1, step=1)
    with col3:
        sets = st.number_input("Sätze", min_value=1, step=1)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Speichern", use_container_width=True):
            st.success(f"✓ Training gespeichert: {weight}kg x {reps} Reps x {sets} Sets")
            st.session_state.training_mode = False
            st.rerun()
    with col2:
        if st.button("❌ Abbrechen", use_container_width=True):
            st.session_state.training_mode = False
            st.rerun()