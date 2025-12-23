import uuid
import streamlit as st

from graph import app
from state import State
from utils.data_store import load_data



st.set_page_config(
    page_title="Health Multi-Agent System",
    layout="centered"
)

st.title("🩺 Health Multi-Agent Assistant")



if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "use_new_user" not in st.session_state:
    st.session_state.use_new_user = False



def get_user_options():
    store = load_data()
    users = store.get("users", {})

    options = {}
    for user_id, info in users.items():
        name = info.get("name", "Unknown")
        label = f"{name} — {user_id[:6]}"
        options[label] = user_id

    return options



st.sidebar.header("User Management")


if st.sidebar.button("➕ Create New User"):
    st.session_state.user_id = str(uuid.uuid4())
    st.session_state.use_new_user = True
    st.sidebar.success("New user created. Enter details below.")


user_options = get_user_options()
selected_user_id = None

if user_options and not st.session_state.use_new_user:
    selected_label = st.sidebar.selectbox(
        "Select existing user",
        options=list(user_options.keys())
    )
    selected_user_id = user_options[selected_label]


active_user_id = (
    st.session_state.user_id
    if st.session_state.use_new_user
    else selected_user_id or st.session_state.user_id
)



st.sidebar.header("Log Health Data")

name = st.sidebar.text_input("Name")

meals = st.sidebar.number_input(
    "Number of meals", min_value=0, max_value=10, step=1
)

water = st.sidebar.number_input(
    "Water intake (liters)", min_value=0.0, step=0.1
)

workout = st.sidebar.number_input(
    "Workout (hours)", min_value=0.0, step=0.5
)

sleep = st.sidebar.number_input(
    "Sleep (hours)", min_value=0.0, step=0.5
)

blood_glucose = st.sidebar.number_input(
    "Blood glucose (mg/dL)",
    min_value=50.0,
    max_value=400.0,
    step=1.0
)

blood_pressure = st.sidebar.text_input(
    "Blood pressure (e.g. 120/80)"
)

medications = st.sidebar.text_area(
    "Medications"
)

mood_stress_anxiety = st.sidebar.text_area(
    "Mood/Stress/Anxiety (describe your feelings here)"
)

symptoms = st.sidebar.text_area(
    "Symptoms (optional)"
)

if st.sidebar.button("Save Health Data"):
    sidebar_input = {
        "name": name,
        "meals": meals,
        "water_intake": water,
        "workout_hours": workout,
        "sleep_hours": sleep,
        "blood_glucose": blood_glucose,
        "blood_pressure": blood_pressure,
        "medications": medications,
        "mood/stress/anxiety": mood_stress_anxiety,
        "symptoms": symptoms,
    }

    state: State = {
        "user_id": active_user_id,
        "sidebar_input": sidebar_input,
    }

    result = app.invoke(state)

    
    st.session_state.use_new_user = False

    st.sidebar.success(result.get("final_response", "Data saved."))




st.subheader("Ask a question")

user_query = st.text_input(
    "Ask about your health data or general health questions"
)

if user_query:
    state: State = {
        "user_id": active_user_id,
        "user_query": user_query,
    }

    result = app.invoke(state)

    st.markdown("### Response")
    st.write(result.get("final_response", "No response generated."))
