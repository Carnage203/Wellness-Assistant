from state import State
from langchain_core.prompts import ChatPromptTemplate
from llm_client import gemini_client, groq_client

def create_healthagent_chain():
    """Create a HealthAgent chain."""

    HealthAgent_Prompt = ChatPromptTemplate.from_messages([
        ("system",
         """You are a Brain Health Agent that manages a team of agents:
            1. IngestionAgent
                - Used when the user provides or logs health data
                - Example: water intake, sleep hours, mood, sugar level

            2. AnalyticsAgent
                - Used when the user asks about patterns, trends, summaries, tracking, medical/health history
                - Example: averages, last week, progress, comparison

            3. HealthQAgent
                - Used for general health-related questions
                - Example: "Can I eat rice at night?", "Is walking good for health?"

            Your job:
                - Read the user's query
                - Decide which ONE agent should act next
                - If no further action is needed, respond with DONE

            Rules:
                - If the user is providing data → IngestionAgent
                - If the user is asking about their past data → AnalyticsAgent
                - If the user is asking a general health question → HealthQAgent
                - If nothing more is required → DONE


            Respond with ONLY ONE of:
            IngestionAgent | AnalyticsAgent | HealthQAgent | DONE

            Do NOT explain your choice.
            Do NOT add extra text.

        """),
        ("human", "{user_query}")
    ])
    
    def run_chain(user_query: str) -> str:
        formatted_prompt = HealthAgent_Prompt.format(user_query=user_query)
        return groq_client.invoke(formatted_prompt)
    
    return run_chain

healthagent_chain = create_healthagent_chain()

def brain_agent(state: State):
    """BrainAgent node for LangGraph.
    Uses HealthAgent chain to decide next agent"""

    user_query = state.get("user_query", "")

    if state.get("sidebar_input"):
        state["next_agent"] = "IngestionAgent"
        return state
    
    decision = healthagent_chain(user_query).strip()

    decision_upper = decision.upper()

    if decision_upper == "DONE":
        state["task_complete"] = True
        return state

    if decision == "IngestionAgent":
        state["next_agent"] = "IngestionAgent"

    elif decision == "AnalyticsAgent":
        state["next_agent"] = "AnalyticsAgent"

    elif decision == "HealthQAgent":
        state["next_agent"] = "HealthQAgent"

    else:
        state["next_agent"] = "HealthQAgent"

    return state
    