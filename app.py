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

def load_user_data(self, file_name, initial_value=None, **load_args):

def save_app_data(self, data, file_name):


pg_homepage = st.Page("views/homepage.py", title="Home", icon=":material/home:", default=True)
pg_workout_selection = st.Page("views/workout_selection.py", title="Workout Auswahl", icon=":material/info:")
pg_upper_exercise_selection = st.Page("views/upper_exercise_selection.py", title="Oberkörper Übungen", icon=":material/info:")
pg_lower_exercise_selection = st.Page("views/lower_exercise_selection.py", title="Unterkörper Übungen", icon=":material/info:")
pg_upper_e1 = st.Page("views/upper_e1.py", title="Oberkörper Übung 1", icon=":material/info:")
pg_upper_e2 = st.Page("views/upper_e2.py", title="Oberkörper Übung 2", icon=":material/info:")
pg_upper_e3 = st.Page("views/upper_e3.py", title="Oberkörper Übung 3", icon=":material/info:")
pg_lower_e1 = st.Page("views/lower_e1.py", title="Unterkörper Übung 1", icon=":material/info:")
pg_lower_e2 = st.Page("views/lower_e2.py", title="Unterkörper Übung 2", icon=":material/info:")
pg_lower_e3 = st.Page("views/lower_e3.py", title="Unterkörper Übung 3", icon=":material/info:")



pg = st.navigation([pg_homepage, pg_workout_selection, 
                    pg_upper_exercise_selection, pg_lower_exercise_selection, 
                    pg_upper_e1, pg_upper_e2, pg_upper_e3, pg_lower_e1, 
                    pg_lower_e2, pg_lower_e3])
pg.run()