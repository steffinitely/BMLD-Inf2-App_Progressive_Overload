import streamlit as st
from functions.progression import calculate_training_volume, get_suggested_weight

st.title("🏋️ Progressive Overload")

st.markdown("""
**Progressive Overload** bedeutet, dass du dein Training systematisch steigerst, um stärker zu werden und Fortschritt zu erzielen.

Ohne Steigerung passt sich dein Körper nicht an. Steigerung kann durch folgende Faktoren erreicht werden:
""")

st.info("""
- mehr Gewicht  
- mehr Wiederholungen  
- mehr Sätze  
""")

st.markdown("""
### 🔬 Wie funktioniert das?

Effektives Training basiert auf messbarer Leistung.

Wenn du deine Gewichte trackst und dich regelmäßig steigerst, setzt du den optimalen Reiz für Muskelaufbau.
""")

st.markdown("""
### 🚀 Wie hilft dir die App?
""")

st.info("""
- speichert dein letztes Training  
- berechnet dein nächstes Gewicht (+2.5%)  
- zeigt dir deinen Fortschritt  
""")

st.markdown("""
### 🎯 Ziel

- Kein Rechnen mehr  
- Kein Raten mehr  
- Klare Progression  

👉 Einfach strukturiert trainieren und stärker werden.
""")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("🏋️ Training starten", use_container_width=True):
        st.switch_page("views/workout_selection.py")
with col2:
    if st.button("📊 Meine Statistiken", use_container_width=True):
        st.info("Statistiken-Seite wird noch entwickelt")