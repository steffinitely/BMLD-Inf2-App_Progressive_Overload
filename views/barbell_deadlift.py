import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_manager import DataManager
from datetime import datetime
from functions.progression import calculate_training_volume, get_suggested_weight

st.title("🏋️ Barbell Deadlift")

st.markdown("""
Barbell Deadlift ist eine fundamentale Ganzkörperübung und einer der stärksten Muskelaufbaureiße.

**Muskeln:**
- Unterer Rücken - Hauptmuskel
- Oberer Rücken
- Beine (Quadrizeps, Hamstrings)
- Gesäß
""")

st.divider()

# Fortschritte aus persistentem data_df laden
data_df = st.session_state.get('data_df', pd.DataFrame())
exercise_name = "Barbell Deadlift"

if not data_df.empty and "exercise" in data_df.columns:
    exercise_data = data_df[data_df['exercise'] == exercise_name].copy()
    if not exercise_data.empty:
        st.subheader("📊 Deine Fortschritte")
        
        # Tabelle mit letzten Trainings
        df_display = exercise_data[["timestamp", "weight", "reps", "sets", "difficulty"]].copy()
        df_display = df_display.sort_values("timestamp", ascending=False).head(10)
        df_display.columns = ["Datum", "Gewicht (kg)", "Wiederholungen", "Sätze", "Schwierigkeit"]
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Graph mit Gewichtsverlauf
        df_graph = exercise_data.sort_values("timestamp", ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_graph["timestamp"],
            y=df_graph["weight"],
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
        st.info("Keine Trainings vorhanden. Erfassen Sie ein neues Training!")
else:
    st.info("Keine Trainings vorhanden. Erfassen Sie ein neues Training!")

st.divider()

# Training-Formular immer sichtbar
st.subheader("➕ Neues Training erfassen")

# Berechne vorgeschlagenes Gewicht basierend auf letztem Training
suggested_weight = get_suggested_weight(exercise_name, data_df)

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
                "exercise": "Barbell Deadlift",
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
            
            st.success(f"✓ Training gespeichert: {weight}kg x {reps} Reps x {sets} Sets - {difficulty}")
            st.rerun()
    with col2:
        if st.button("❌ Abbrechen", use_container_width=True):
            st.rerun()

st.divider()

if st.button("← Zurück zur Auswahl", use_container_width=True):
    st.switch_page("views/lower_exercise_selection.py")