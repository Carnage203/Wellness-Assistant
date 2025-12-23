# Health Multi-Agent System

## 📋 Project Overview

This project is a **Multi-Agent AI Health Tracking & Query System** designed to simulate how AI agents collaborate to handle health tracking, reasoning, and analytics. It allows users to log daily health metrics, ask general health questions, and receive personalized insights along with tracking based on their historical data.

The system is built using **LangGraph** for agent orchestration, **Streamlit** for the user interface, and leverages **Google Gemini** and **Groq (Llama 3)** for intelligence.

## 🚀 Features

### 1. Health Data Tracking (Ingestion Agent)

Log comprehensive daily health data including:

- 🍎 **Meals & Nutrition**
- 💧 **Water Intake**
- 🏃 **Workout & Physical Activity**
- 😴 **Sleep Duration**
- 🩸 **Blood Glucose & Blood Pressure**
- 🧘 **Mood & Symptoms**

### 2. General Health Q&A (HealthQ Agent)

Ask general health-related questions such as:

- _"Can I eat curd at night?"_
- _"Is walking good for diabetes?"_
- _"How much sleep do I need?"_

### 3. Smart Analytics (Analytics Agent)

Gain meaningful insights from your logged data:

- _"How much water have I consumed in the past 7 days?"_
- _"What is my average sleep for this week?"_
- _"Do you see any patterns in my sugar readings?"_

## 🤖 Agent Architecture

The system uses a **Hub-and-Spoke** architecture managed by a central Brain Agent.

1.  **🧠 Brain Agent (Orchestrator)**:

    - Receives user input (questions or data logs).
    - Decides which specialist agent is best suited to handle the request.
    - Routes the task to Ingestion, Analytics, or QA agents.

2.  **📝 Ingestion Agent**:

    - Responsible for saving structured health data into the system's storage.
    - Handles inputs from the sidebar logging form.

3.  **📊 Analytics Agent**:

    - Reads the user's historical data.
    - Uses an LLM to analyze trends, averages, and patterns to answer specific user queries about their history.

4.  **🩺 HealthQ Agent**:
    - Handles general medical and health knowledge queries.
    - Provides evidence-based general information (not medical diagnosis).

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/)
- **LLMs**:
  - Google Gemini 2.5 Flash
  - Llama 3.3 70B (via Groq)
- **Language**: Python 3.11+

## 📁 Project Structure

```
neolen_assignment/
├── agents/                 # Agent implementations
│   ├── brain.py            # Main orchestrator
│   ├── ingestagent.py      # Data saving logic
│   ├── analyticsagent.py   # Data analysis logic
│   └── qaagent.py          # General Q&A logic
├── utils/                  # Helper functions
│   ├── data_store.py       # JSON file handling
│   └── routers.py          # Conditional routing logic
├── data/                   # Data storage
│   └── storage.json        # Local JSON database (auto-generated)
├── main.py                 # Streamlit entry point
├── graph.py                # LangGraph workflow definition
├── state.py                # Shared state definition
├── llm_client.py           # API client wrappers
└── requirements.txt        # Dependencies
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd neolen_assignment
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```ini
GEMINI_API_KEY=your_google_gemini_key
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the Application

```bash
streamlit run main.py
```

## 📖 Usage Guide

1.  **Create a User**: Use the sidebar to create a new user profile or select an existing one.
2.  **Log Data**: Fill out the health metrics in the sidebar and click "Save Health Data". The **IngestionAgent** will process this.
3.  **Ask Questions**: Use the main chat input to:
    - Ask general questions (routed to **HealthQAgent**).
    - Ask about your past data (routed to **AnalyticsAgent**).

## 📄 License

This project is created for an assignment and is open for educational use.
