import streamlit as st

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/unterseite_a.py", title="Unterseite A", icon=":material/info:")

pg = st.navigation([pg_home, pg_second])
pg.run()

# app.py

import streamlit as st
from functions.progression import calculate_progression, calculate_training_volume, get_last_entry

st.set_page_config(page_title="Progressive Overload")

# ------------------------
# Session State initialisieren
# ------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "workouts" not in st.session_state:
    st.session_state.workouts = []

# ------------------------
# Navigation Funktionen
# ------------------------
def go_to(page):
    st.session_state.page = page

# ------------------------
# HOME
# ------------------------
if st.session_state.page == "home":
    st.title("🏋️ Progressive Overload")

    st.button("Log In", on_click=go_to, args=("login",))
    st.button("Sign Up", on_click=go_to, args=("signup",))
    st.button("Info", on_click=go_to, args=("info",))

# ------------------------
# SIGN UP
# ------------------------
elif st.session_state.page == "signup":
    st.title("Sign Up")

    name = st.text_input("Name")
    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")

    if st.button("Registrieren"):
        st.success("Account erstellt (Dummy)")
        go_to("login")

# ------------------------
# LOGIN
# ------------------------
elif st.session_state.page == "login":
    st.title("Log In")

    username = st.text_input("Username")
    password = st.text_input("Passwort", type="password")

    if st.button("Einloggen"):
        st.success("Erfolgreich eingeloggt (Dummy)")
        go_to("split")

# ------------------------
# INFO SCREEN
# ------------------------
elif st.session_state.page == "info":
    st.title("Was ist Progressive Overload?")

    st.write("""
    Progressive Overload bedeutet, dass du dein Training kontinuierlich steigerst,
    um stärker zu werden. Das kann durch mehr Gewicht, mehr Wiederholungen oder mehr Sätze passieren.
    """)

    st.button("Zurück", on_click=go_to, args=("home",))

# ------------------------
# SPLIT AUSWAHL
# ------------------------
elif st.session_state.page == "split":
    st.title("Wähle deinen Split")

    st.button("Oberkörper", on_click=go_to, args=("oberkoerper",))
    st.button("Unterkörper", on_click=go_to, args=("unterkoerper",))

# ------------------------
# ÜBUNGSLISTE
# ------------------------
elif st.session_state.page == "oberkoerper":
    st.title("Oberkörper")

    if st.button("Übung 1"):
        st.session_state.exercise = "Übung 1"
        go_to("exercise")

    if st.button("Übung 2"):
        st.session_state.exercise = "Übung 2"
        go_to("exercise")

    if st.button("Zurück"):
        go_to("split")


elif st.session_state.page == "unterkoerper":
    st.title("Unterkörper")

    if st.button("Übung 1"):
        st.session_state.exercise = "Übung 1"
        go_to("exercise")

    if st.button("Übung 2"):
        st.session_state.exercise = "Übung 2"
        go_to("exercise")

    if st.button("Zurück"):
        go_to("split")

# ------------------------
# ÜBUNG DETAIL / LOGGING
# ------------------------
elif st.session_state.page == "exercise":
    st.title(f"{st.session_state.exercise}")

    weight = st.number_input("Gewicht (kg)", min_value=0.0)
    reps = st.number_input("Reps", min_value=0)
    sets = st.number_input("Sets", min_value=0)

    last_entry = get_last_entry(st.session_state.workouts)

    if last_entry:
        st.subheader("Letztes Training")
        st.write(last_entry)

        suggestion = calculate_progression(last_entry["weight"])
        st.write(f"Vorschlag: {suggestion} kg")

    if st.button("Speichern"):
        entry = {
            "exercise": st.session_state.exercise,
            "weight": weight,
            "reps": reps,
            "sets": sets,
            "volume": calculate_training_volume(weight, reps, sets)
        }

        st.session_state.workouts.append(entry)
        st.success("Workout gespeichert")

    if st.button("Zurück"):
        go_to("split")