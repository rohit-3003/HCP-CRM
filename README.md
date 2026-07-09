# AI-First CRM HCP Module

An enterprise-grade, AI-first Customer Relationship Management (CRM) system module for field representatives to log interactions with Healthcare Professionals (HCPs). 

This project was built focusing on an "AI-First" paradigm, shifting from traditional CRUD data entry to conversational, context-aware interaction powered by a LangGraph AI Agent.

## Architecture & Tech Stack

**Frontend:** React (Vite), Redux Toolkit, Vanilla CSS (Google Inter font)
**Backend:** Python, FastAPI, LangGraph, Langchain
**LLM:** Groq (`llama-3.1-8b-instant` - *Note: `gemma2-9b-it` was decommissioned by Groq on July 2026, so the code dynamically uses a modern fallback that ensures compliance and reliability.*)
**Database:** PostgreSQL (SQLAlchemy ORM)
**Infrastructure:** Docker Compose

## Screenshots

*(Note: Replace these placeholders with actual screenshots before submission)*

### Dashboard & UI
![Dashboard](./assets/dashboard.png)

### Chat Interface
![Chat Interface](./assets/chat_interface.png)

### Structured Form
![Structured Form](./assets/structured_form.png)

### AI Insights Panel
![AI Insights Panel](./assets/ai_insights.png)

### Swagger UI (Backend)
![Swagger UI](./assets/swagger_ui.png)

### Docker Containers
![Docker Containers Running](./assets/docker_containers.png)

### System Architecture Diagram

```text
                   React + Redux

     Structured Form      AI Chat Interface     Dashboard
             │                   │                  │
             └───────────┬───────┴──────────────────┘
                         │
                   FastAPI Backend
                         │
                  LangGraph Agent (Groq LLM)
                         │
      ┌────────────┬────────────┬────────────┐
      │            │            │            │
  Intent      Entity      Router       Memory
 Detection    Extraction                 State
      │            │            │
      └────────────┴────────────┘
                    │
              LangGraph Tools
                    │
     ┌────────┬────────┬────────┬────────┬────────┐
     │        │        │        │        │        │
    Log      Edit     HCP   Follow-up  Materials
     │
 PostgreSQL (via SQLAlchemy)
```

## AI-First Features

1. **Conversational Logging:** Instead of filling forms, reps can just chat: "Met with Dr. Sharma for 15 mins. Discussed CardioPlus, she was interested. Schedule a follow-up for next week."
2. **True StateGraph Memory:** The LangGraph agent maintains a history of the conversation, allowing follow-ups like "Actually, change the duration to 30 mins."
3. **Automatic Entity Extraction & Sentiment Analysis:** The agent extracts HCP names, topics, duration, and gauges the sentiment of the interaction automatically.
4. **AI Insights Panel:** A premium frontend UI (inspired by Microsoft Copilot) visually displays the agent's real-time thoughts, extracted entities, confidence scores, and missing information.

## The 5 LangGraph Tools

1. `tool_log_interaction`: Captures and structures interaction data.
2. `tool_edit_interaction`: Modifies logged data based on contextual memory.
3. `tool_get_hcp_profile`: Retrieves detailed background info on an HCP.
4. `tool_schedule_followup`: Schedules a follow-up task.
5. `tool_search_materials`: Queries the seeded Materials table for relevant literature based on the chat.

## Running the Application

### Prerequisites
- Docker and Docker Compose installed.
- A valid Groq API Key.

### Setup Instructions

1. **Clone the repository.**
2. **Add your API Key:**
   Create a `.env` file in the root directory (or in `backend/`) and add:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

This will spin up:
- **PostgreSQL Database** on port `5432` (automatically seeded with realistic data).
- **FastAPI Backend** on `http://localhost:8000`. 
  - *Swagger API Docs available at `http://localhost:8000/docs`*
- **React Frontend** on `http://localhost:5173`.

## Future Improvements
- **Authentication:** Integrate OAuth2 for field rep login.
- **Voice-to-Text:** Allow reps to dictate their interactions instead of typing.
- **Complex Analytics:** Expand the dashboard with historical charting.
