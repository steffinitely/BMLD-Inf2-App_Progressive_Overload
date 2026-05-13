import streamlit as st
from functions.progression import calculate_training_volume, get_suggested_weight

st.title("🏋️ Progressive Overload")

st.markdown("""
**Progressive Overload** bedeutet, dass du dein Training systematisch steigerst, um stärker zu werden und Fortschritte zu erzielen.

Ohne eine Steigerung passt sich dein Körper nicht an. Diese Steigerung kann durch folgende Faktoren erreicht werden:
""")

st.info("""
- Mehr Gewicht  
- Mehr Wiederholungen  
- Mehr Sätze  
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
- Speichert dein letztes Training  
- Empfiehlt dir Gewicht / Wiederholungen basierend auf deinem Feedback
- Berechnet dein nächstes Gewicht (+2.5%)  
- Zeigt dir deinen Fortschritt in einer Tabelle und Grafik 
""")

st.markdown("""
### 🎯 Ziel

- Kein Rechnen mehr  
- Kein Raten mehr  
- Klare Progression  

👉 Einfach strukturiert trainieren und stärker werden ohne grosse Anstrengung.
""")

st.divider()

col1, col2 = st.columns(2)
with col1:
    if st.button("🏋️ Training starten", use_container_width=True):
        st.switch_page("views/workout_selection.py")
with col2:
    if st.button("📊 Meine Statistiken", use_container_width=True):
        st.info("Statistiken-Seite wird noch entwickelt")