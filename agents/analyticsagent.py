from state import State
from llm_client import gemini_client, groq_client
from utils.data_store import load_data

def AnalyticsAgent(state: State):
    """Agent responsible for analyzing user health data and providing insights."""
    user_id = state.get("user_id")

    if not user_id:
        state["final_response"] = "User ID not provided. Cannot analyze data."
        state["task_complete"] = True
        return state
    
    user_query = state.get("user_query", "")

    store = load_data()
    users = store.get("users", {})

    if user_id not in users:
        state["final_response"] = "No data found for this user."
        state["task_complete"] = True
        return state

    user_data = users[user_id]

    prompt = f"""
             You are a health analytics agent. Based on the user's historical health data, Only provide the analytical insights and tracking related requested.
             RULES:
                - Use ONLY the data provided below.
                - Answer ONLY what the user explicitly asked.
                - If data is missing, say so.
                - Provide analytical insights and tracking.
                - For comparative questions about whether a metric is "sufficient" or "normal", respond succinctly with "Yes" or "No" followed by a one-line rationale comparing the user's value to commonly accepted general ranges or guidance; if required data is missing reply "Insufficient data" and state what is missing.
                - Avoid medical advice or diagnosis; if values appear outside typical ranges, recommend consulting a healthcare professional.
                - Be concise.
             User Query:
             {user_query}
             User Health Data:
             {user_data}
             
            """
    
    response = groq_client.invoke(prompt)

    state["final_response"] = response
    state["task_complete"] = True
    return state