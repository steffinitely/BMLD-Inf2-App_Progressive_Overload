import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from functions.progression import calculate_progression, calculate_training_volume
from datetime import datetime

st.set_page_config(page_title="Statistiken", layout="wide")
st.title("📊 Deine Trainingsstatistiken")

# Daten aus Session State laden
if 'data_df' not in st.session_state or st.session_state['data_df'].empty:
    st.warning("Keine Trainingsdaten vorhanden. Fügen Sie zunächst einige Workouts hinzu!")
    st.stop()

df = st.session_state['data_df'].copy()

# Stelle sicher, dass timestamp als datetime definiert ist
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['datum'] = df['timestamp'].dt.date
else:
    if 'datum' in df.columns:
        df['datum'] = pd.to_datetime(df['datum']).dt.date
    else:
        st.error("Keine Zeitstempel in den Daten gefunden!")
        st.stop()

# Stelle sicher, dass wichtige numerische Spalten vorhanden sind
required_cols = ['exercise', 'weight', 'reps', 'sets']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    st.error(f"Fehlende Spalten in den Daten: {missing_cols}")
    st.stop()

# Trainingsvolumen berechnen
df['volume'] = df.apply(
    lambda row: calculate_training_volume(row['weight'], row['reps'], row['sets']),
    axis=1
)

# Übersicht aller Übungen
st.subheader("🏋️ Verfügbare Übungen")
unique_exercises = df['exercise'].unique()
st.info(f"Anzahl der Übungen: {len(unique_exercises)} | Anzahl der Einträge: {len(df)}")

# Tabs für verschiedene Ansichten
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Gewichtsverlauf", 
    "📊 Trainingsvolumen", 
    "🎯 Fortschrittsübersicht",
    "📋 Alle Daten"
])

# ==================== TAB 1: GEWICHTSVERLAUF ====================
with tab1:
    st.subheader("Gewichtsverlauf pro Übung")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_exercise = st.selectbox(
            "Wähle eine Übung:",
            unique_exercises,
            key="exercise_select"
        )
    
    # Daten der ausgewählten Übung filtern
    df_exercise = df[df['exercise'] == selected_exercise].copy()
    df_exercise = df_exercise.sort_values('timestamp') if 'timestamp' in df_exercise.columns else df_exercise.sort_values('datum')
    
    if not df_exercise.empty:
        # Statistische Übersicht
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Höchstes Gewicht", f"{df_exercise['weight'].max():.1f} kg")
        with col2:
            st.metric("Niedrigstes Gewicht", f"{df_exercise['weight'].min():.1f} kg")
        with col3:
            st.metric("Durchschnitt", f"{df_exercise['weight'].mean():.1f} kg")
        with col4:
            latest_weight = df_exercise['weight'].iloc[-1]
            first_weight = df_exercise['weight'].iloc[0]
            progress = ((latest_weight - first_weight) / first_weight * 100) if first_weight > 0 else 0
            st.metric("Fortschritt", f"{progress:+.1f}%")
        
        st.divider()
        
        # Liniendiagramm für Gewichtsverlauf
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_exercise['timestamp'] if 'timestamp' in df_exercise.columns else df_exercise['datum'],
            y=df_exercise['weight'],
            mode='lines+markers',
            name='Gewicht (kg)',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8),
            hovertemplate='<b>%{x}</b><br>Gewicht: %{y:.1f} kg<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Gewichtsverlauf: {selected_exercise}",
            xaxis_title="Datum",
            yaxis_title="Gewicht (kg)",
            hovermode='x unified',
            height=450,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabelle mit letzten Einträgen
        st.subheader("Letzte 10 Trainings")
        df_display = df_exercise[['datum', 'weight', 'reps', 'sets', 'volume']].copy() if 'datum' in df_exercise.columns else df_exercise[['timestamp', 'weight', 'reps', 'sets', 'volume']].copy()
        df_display = df_display.tail(10).sort_values(df_display.index[0], ascending=False)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.warning(f"Keine Daten für die Übung '{selected_exercise}' vorhanden.")

# ==================== TAB 2: TRAININGSVOLUMEN ====================
with tab2:
    st.subheader("Trainingsvolumen nach Übung")
    
    # Gesamtvolumen pro Übung
    volume_by_exercise = df.groupby('exercise')['volume'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Balkendiagramm
        fig_volume = px.bar(
            x=volume_by_exercise.index,
            y=volume_by_exercise.values,
            labels={'x': 'Übung', 'y': 'Gesamtvolumen (kg × Reps × Sets)'},
            title="Gesamttrainingsvolumen pro Übung"
        )
        fig_volume.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        # Kreisdiagramm
        fig_pie = px.pie(
            values=volume_by_exercise.values,
            names=volume_by_exercise.index,
            title="Volumenverteilung"
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()
    
    # Volumen über Zeit für alle Übungen
    st.subheader("Kumulatives Trainingsvolumen über Zeit")
    
    # Gruppieren nach Datum und Übung
    df_volume_time = df.groupby([df['timestamp'] if 'timestamp' in df.columns else df['datum'], 'exercise'])['volume'].sum().reset_index()
    df_volume_time.columns = ['datum', 'exercise', 'volume']
    
    fig_volume_time = px.line(
        df_volume_time,
        x='datum',
        y='volume',
        color='exercise',
        title="Trainingsvolumen pro Workout (nach Übung)",
        labels={'datum': 'Datum', 'volume': 'Volumen', 'exercise': 'Übung'}
    )
    fig_volume_time.update_layout(height=450, template='plotly_white')
    st.plotly_chart(fig_volume_time, use_container_width=True)

# ==================== TAB 3: FORTSCHRITTSÜBERSICHT ====================
with tab3:
    st.subheader("Fortschrittsübersicht aller Übungen")
    
    progress_data = []
    
    for exercise in unique_exercises:
        df_ex = df[df['exercise'] == exercise].copy()
        if not df_ex.empty:
            df_ex_sorted = df_ex.sort_values('timestamp') if 'timestamp' in df_ex.columns else df_ex.sort_values('datum')
            
            first_weight = df_ex_sorted['weight'].iloc[0]
            last_weight = df_ex_sorted['weight'].iloc[-1]
            max_weight = df_ex_sorted['weight'].max()
            avg_weight = df_ex_sorted['weight'].mean()
            total_volume = df_ex_sorted['volume'].sum()
            num_workouts = len(df_ex)
            
            progress_pct = ((last_weight - first_weight) / first_weight * 100) if first_weight > 0 else 0
            
            first_date = df_ex_sorted['timestamp'].min() if 'timestamp' in df_ex_sorted.columns else pd.Timestamp(df_ex_sorted['datum'].min())
            last_date = df_ex_sorted['timestamp'].max() if 'timestamp' in df_ex_sorted.columns else pd.Timestamp(df_ex_sorted['datum'].max())
            days_trained = (last_date - first_date).days + 1
            
            progress_data.append({
                'Übung': exercise,
                'Erste Last (kg)': f"{first_weight:.1f}",
                'Aktuelle Last (kg)': f"{last_weight:.1f}",
                'Gewichtzunahme (%)': f"{progress_pct:+.1f}%",
                'Max. Gewicht (kg)': f"{max_weight:.1f}",
                'Ø Gewicht (kg)': f"{avg_weight:.1f}",
                'Anzahl Workouts': num_workouts,
                'Gesamtvolumen': f"{total_volume:.0f}",
                'Tage': days_trained
            })
    
    if progress_data:
        progress_df = pd.DataFrame(progress_data)
        st.dataframe(progress_df, use_container_width=True, hide_index=True)
        
        # Visualisierung: Fortschritt in Prozent
        st.divider()
        st.subheader("Gewichtszunahme pro Übung")
        
        # Extrahiere numerische Werte für Visualisierung
        progress_for_viz = []
        for data in progress_data:
            progress_pct_str = data['Gewichtzunahme (%)'].replace('%', '').replace('+', '')
            progress_for_viz.append({
                'Übung': data['Übung'],
                'Fortschritt': float(progress_pct_str)
            })
        
        progress_viz_df = pd.DataFrame(progress_for_viz)
        
        fig_progress = px.bar(
            progress_viz_df,
            x='Übung',
            y='Fortschritt',
            color='Fortschritt',
            color_continuous_scale=['red', 'green'],
            title="Gewichtszunahme seit Anfang (%)",
            labels={'Fortschritt': 'Fortschritt (%)'}
        )
        fig_progress.update_layout(height=400, template='plotly_white')
        st.plotly_chart(fig_progress, use_container_width=True)
    else:
        st.warning("Keine Fortschrittsdaten verfügbar.")

# ==================== TAB 4: ALLE DATEN ====================
with tab4:
    st.subheader("Alle Trainingsdaten")
    
    # Sortieren und Anzeigen
    if 'timestamp' in df.columns:
        df_display = df.sort_values('timestamp', ascending=False)
        display_cols = ['timestamp', 'exercise', 'weight', 'reps', 'sets', 'volume']
    else:
        df_display = df.sort_values('datum', ascending=False)
        display_cols = ['datum', 'exercise', 'weight', 'reps', 'sets', 'volume']
    
    # Nur verfügbare Spalten anzeigen
    display_cols = [col for col in display_cols if col in df_display.columns]
    
    st.dataframe(df_display[display_cols], use_container_width=True, hide_index=True)
    
    # Download-Option
    csv = df_display.to_csv(index=False)
    st.download_button(
        label="📥 Daten als CSV herunterladen",
        data=csv,
        file_name=f"trainingsstatistiken_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

st.divider()

# Footer Navigation
col1, col2 = st.columns(2)
with col1:
    if st.button("← Zurück zur Startseite", use_container_width=True):
        st.switch_page("views/homepage.py")
