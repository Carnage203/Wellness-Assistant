from state import State
from datetime import date
from utils.data_store import load_data, save_data

def IngestionAgent(state: State):
    """Agent responsible for ingesting user-provided health data into the system."""
    input_data = state.get("sidebar_input", {})
    user_id = state.get("user_id")

    if not input_data:
        state["final_response"] = "No data provided for ingestion."
        state["task_complete"] = True
        return state

    today = str(date.today())
    stored_data = load_data()

    if "users" not in stored_data:
        stored_data["users"] = {}

    if user_id not in stored_data["users"]:
        stored_data["users"][user_id] = {
            "name": input_data.get("name", "Unknown"),
            "records": {}
        }

    stored_data["users"][user_id]["records"][today] = {
        "meals": input_data.get("meals"),
        "water_intake": input_data.get("water_intake"),
        "workout_hours": input_data.get("workout_hours"),
        "sleep_hours": input_data.get("sleep_hours"),
        "blood_glucose": input_data.get("blood_glucose"),
        "blood_pressure": input_data.get("blood_pressure"),
        "medications": input_data.get("medications"),
        "mood/stress/anxiety": input_data.get("mood/stress/anxiety"),
        "symptoms": input_data.get("symptoms"),
    }

    save_data(stored_data)

    state["final_response"] = "Your health data has been successfully ingested."
    state["task_complete"] = True

    state.pop("sidebar_input", None)

    return state