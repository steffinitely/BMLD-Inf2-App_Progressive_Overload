import streamlit as st

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

pg_homepage = st.Page("views/homepage.py", title="Home", icon=":material/home:", default=True)
pg_login= st.Page("views/login.py", title="Login", icon=":material/info:")
pg_signup = st.Page("views/signup.py", title="Sign Up", icon=":material/info:")
pg_workout_selection = st.Page("views/workout_selection.py", title="Workout Auswahl", icon=":material/info:")
pg_upper_exercise_selection = st.Page("views/upper_exercise_selection.py", title="Oberkörper Übungen", icon=":material/info:")
pg_lower_exercise_selection = st.Page("views/lower_exercise_selection.py", title="Unterkörper Übungen", icon=":material/info:")
pg_upper_e1 = st.Page("views/upper_e1.py", title="Oberkörper Übung 1", icon=":material/info:")
pg_upper_e1_weight = st.Page("views/upper_e1_weight.py", title="Oberkörper Übung 1 Gewicht", icon=":material/info:")
pg_upper_e1_stat = st.Page("views/upper_e1_stat.py", title="Oberkörper Übung 1 Stats", icon=":material/info:")
pg_upper_e2 = st.Page("views/upper_e2.py", title="Oberkörper Übung 2", icon=":material/info:")
pg_upper_e2_weight = st.Page("views/upper_e2_weight.py", title="Oberkörper Übung 2 Gewicht", icon=":material/info:")
pg_upper_e2_stat = st.Page("views/upper_e2_stat.py", title="Oberkörper Übung 2 Stats", icon=":material/info:")
pg_upper_e3 = st.Page("views/upper_e3.py", title="Oberkörper Übung 3", icon=":material/info:")
pg_upper_e3_weight = st.Page("views/upper_e3_weight.py", title="Oberkörper Übung 3 Gewicht", icon=":material/info:")
pg_upper_e3_stat = st.Page("views/upper_e3_stat.py", title="Oberkörper Übung 3 Stats", icon=":material/info:")
pg_lower_e1 = st.Page("views/lower_e1.py", title="Unterkörper Übung 1", icon=":material/info:")
pg_lower_e1_weight = st.Page("views/lower_e1_weight.py", title="Unterkörper Übung 1 Gewicht", icon=":material/info:")
pg_lower_e1_stat = st.Page("views/lower_e1_stat.py", title="Unterkörper Übung 1 Stats", icon=":material/info:")
pg_lower_e2 = st.Page("views/lower_e2.py", title="Unterkörper Übung 2", icon=":material/info:")
pg_lower_e2_weight = st.Page("views/lower_e2_weight.py", title="Unterkörper Übung 2 Gewicht", icon=":material/info:")
pg_lower_e2_stat = st.Page("views/lower_e2_stat.py", title="Unterkörper Übung 2 Stats", icon=":material/info:")
pg_lower_e3 = st.Page("views/lower_e3.py", title="Unterkörper Übung 3", icon=":material/info:")
pg_lower_e3_weight = st.Page("views/lower_e3_weight.py", title="Unterkörper Übung 3 Gewicht", icon=":material/info:")
pg_lower_e3_stat = st.Page("views/lower_e3_stat.py", title="Unterkörper Übung 3 Stats", icon=":material/info:")



pg = st.navigation([pg_homepage, pg_login, pg_signup, pg_workout_selection, pg_upper_exercise_selection, pg_lower_exercise_selection, pg_upper_e1, pg_upper_e1_weight, pg_upper_e1_stat, pg_upper_e2, pg_upper_e2_weight, pg_upper_e2_stat, pg_upper_e3, pg_upper_e3_weight, pg_upper_e3_stat, pg_lower_e1, pg_lower_e1_weight, pg_lower_e1_stat, pg_lower_e2, pg_lower_e2_weight, pg_lower_e2_stat, pg_lower_e3, pg_lower_e3_weight, pg_lower_e3_stat])
pg.run()