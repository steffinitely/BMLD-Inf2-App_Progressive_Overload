import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

data_manager = DataManager(fs_protocol='webdav', fs_root_folder='overload')
login_manager = LoginManager(data_manager)
login_manager.login_register()

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame(),
        parse_dates=['timestamp'])


pg_homepage = st.Page("views/homepage.py", title="Home", icon=":material/home:", default=True)
pg_workout_selection = st.Page("views/workout_selection.py", title="Workout Auswahl", icon=":material/info:")
pg_upper_exercise_selection = st.Page("views/upper_exercise_selection.py", title="Oberkörper Übungen", icon=":material/info:")
pg_lower_exercise_selection = st.Page("views/lower_exercise_selection.py", title="Unterkörper Übungen", icon=":material/info:")
pg_barbell_benchpress = st.Page("views/barbell_benchpress.py", title="Barbell Benchpress", icon=":material/info:")
pg_dumbbell_shoulderpress = st.Page("views/dumbbell_shoulderpress.py", title="Dumbbell Shoulder Press", icon=":material/info:")
pg_latpulldown = st.Page("views/latpulldownmachine.py", title="Lat Pulldown", icon=":material/info:")
pg_barbell_deadlift = st.Page("views/barbell_deadlift.py", title="Barbell Deadlift", icon=":material/info:")
pg_barbell_squat = st.Page("views/barbell_squat.py", title="Barbell Squat", icon=":material/info:")
pg_dumbbell_bulgariansquat = st.Page("views/dumbbell_bulgariansquat.py", title="Dumbbell Bulgarian Split Squat", icon=":material/info:")
pg_statistik = st.Page("views/statistik.py", title="Statistiken", icon=":material/analytics:")



pg = st.navigation([pg_homepage, pg_workout_selection,
                    pg_upper_exercise_selection, pg_lower_exercise_selection,
                    pg_barbell_benchpress, pg_dumbbell_shoulderpress, pg_latpulldown, pg_barbell_deadlift,
                    pg_barbell_squat, pg_dumbbell_bulgariansquat, pg_statistik])
pg.run()