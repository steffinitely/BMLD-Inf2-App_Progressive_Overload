import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from functions.progression import calculate_progression, calculate_training_volume, get_last_entry, get_suggested_weight
from utils.data_manager import DataManager
from datetime import datetime

if "training_mode" not in st.session_state:
    st.session_state.training_mode = False

if "bulgariansquat_workouts" not in st.session_state:
    st.session_state.bulgariansquat_workouts = []

st.title("🏋️ Dumbbell Bulgarian Split Squat")

st.markdown("""
Bulgarian Split Squat ist eine hervorragende unilaterale (einseitige) Beinübung für Balance und Muskelaufbau.

**Muskeln:**
- Quadrizeps - Hauptmuskel
- Hamstrings
- Gesäß (Glutes)
- Adduktoren
""")

st.divider()

if not st.session_state.training_mode:
    st.subheader("📊 Deine Fortschritte")
    
    if st.session_state.bulgariansquat_workouts:
        # Pandas Tabelle mit letzten Trainings
        df = pd.DataFrame(st.session_state.bulgariansquat_workouts)
        df = df[["datum", "gewicht", "wiederholungen", "sätze", "schwierigkeit"]].copy()
        df = df.sort_values("datum", ascending=False).head(10)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Graph mit Gewichtsverlauf
        df_sorted = df.sort_values("datum", ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_sorted["datum"],
            y=df_sorted["gewicht"],
            mode='lines+markers',
            name='Gewicht (kg)',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Gewichtsverlauf",
            xaxis_title="Datum",
            yaxis_title="Gewicht (kg)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Keine Trainings vorhanden. Starten Sie ein neues Training!")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Neues Training", use_container_width=True):
            st.session_state.training_mode = True
            st.rerun()
    with col2:
        if st.button("← Zurück", use_container_width=True):
            st.switch_page("views/lower_exercise_selection.py")
else:
    st.subheader("➕ Neues Training erfassen")
    
    # Berechne vorgeschlagenes Gewicht basierend auf letztem Training
    data_df = st.session_state.get('data_df', pd.DataFrame())
    suggested_weight = get_suggested_weight("Dumbbell Bulgarian Split Squat", data_df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        weight = st.number_input("Gewicht (kg)", min_value=0.0, step=0.5, format="%.1f", value=suggested_weight)
    with col2:
        reps = st.number_input("Wiederholungen", min_value=1, step=1)
    with col3:
        sets = st.number_input("Sätze", min_value=1, step=1)
    
    # Schwierigkeits-Rating
    difficulty = st.select_slider(
        "Wie hat sich die Übung angefühlt?",
        options=["Sehr einfach", "Einfach", "Gut", "Schwierig", "Sehr schwierig"],
        value="Gut"
    )
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Speichern", use_container_width=True):
            # Erstelle neues Workout-Record mit exercise Feld
            workout_record = {
                "exercise": "Dumbbell Bulgarian Split Squat",
                "weight": weight,
                "reps": reps,
                "sets": sets,
                "difficulty": difficulty
            }
            
            # Aktualisiere globales DataFrame
            st.session_state['data_df'] = DataManager.append_record(
                st.session_state['data_df'],
                workout_record
            )
            
            # Speichere zu WebDAV/Dateisystem
            data_manager = DataManager()
            data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
            
            # Aktualisiere auch lokale Liste für Anzeige
            local_workout = {
                "datum": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "gewicht": weight,
                "wiederholungen": reps,
                "sätze": sets,
                "schwierigkeit": difficulty
            }
            st.session_state.bulgariansquat_workouts.append(local_workout)
            
            st.success(f"✓ Training gespeichert: {weight}kg x {reps} Reps x {sets} Sets - {difficulty}")
            st.session_state.training_mode = False
            st.rerun()
    with col2:
        if st.button("❌ Abbrechen", use_container_width=True):
            st.session_state.training_mode = False
            st.rerun()