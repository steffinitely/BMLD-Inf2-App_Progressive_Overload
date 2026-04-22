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
