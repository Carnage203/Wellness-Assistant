from langgraph.graph import  StateGraph, END
from state import State
from utils.routers import router
from agents.brain import brain_agent
from agents.ingestagent import IngestionAgent
from agents.analyticsagent import AnalyticsAgent
from agents.qaagent import HealthQAgent

workflow = StateGraph(State)

workflow.add_node("BrainAgent", brain_agent)
workflow.add_node("IngestionAgent", IngestionAgent)
workflow.add_node("AnalyticsAgent", AnalyticsAgent)
workflow.add_node("HealthQAgent", HealthQAgent)

workflow.set_entry_point("BrainAgent")
workflow.add_conditional_edges(
    "BrainAgent",
    router,
    {
        "IngestionAgent": "IngestionAgent",
        "AnalyticsAgent": "AnalyticsAgent",
        "HealthQAgent": "HealthQAgent",
        END: END,
    },
)
workflow.add_edge("IngestionAgent", END)
workflow.add_edge("AnalyticsAgent", END)
workflow.add_edge("HealthQAgent", END)


app = workflow.compile()

# from PIL import Image
# import io
# png_data = app.get_graph().draw_mermaid_png()
# with open("workflow.png", "wb") as f:
#     f.write(png_data)
# img = Image.open(io.BytesIO(png_data))
# img.show() 