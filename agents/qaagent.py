from state import State
from llm_client import gemini_client, groq_client
from utils.data_store import load_data

def HealthQAgent(state: State):
    """Agent responsible for answering general health questions."""
    user_query = state.get("user_query", "")
    user_id = state.get("user_id")
    if not user_id:
        state["final_response"] = "User ID not provided. Cannot answer questions."
        state["task_complete"] = True
        return state
    store = load_data()
    users = store.get("users", {})
    if user_id not in users:
        state["final_response"] = "No data found for this user."
        state["task_complete"] = True
        return state
    user_data = users[user_id]
    records = user_data.get("records", {})
    health_history = []
    for date, daily_data in records.items():
        #print(date, daily_data)
        medication = daily_data.get("medications", "").strip()
        symptoms = daily_data.get("symptoms", "").strip()
        #print(medication,symptoms)

        health_history.append({
                "date": date,
                "medications": medication,
                "symptoms": symptoms
        })
    prompt = f"""
        You are a health information assistant. You will answer always answer keeping Health History in context.

        Your role:
        - Answer general health-related questions.
        - Provide safe, evidence-based information, answer with simple yes or no with provided evidence.
        - Do NOT give medical diagnosis or prescriptions.
        - Do NOT make assumptions about the user, Always rely on provided Health History data.

        Guidelines:
        - Never answer any question apart from general health knowledge.
        - Be concise and clear.
        - If the question is outside general health knowledge, say so.
        - If professional consultation is required, mention it briefly.
        - Avoid unnecessary explanations.

        User Question:
        {user_query}
        User Health History:
        {health_history}
        """


    response = groq_client.invoke(prompt)

    state["final_response"] = response
    state["task_complete"] = True
    return state