# Google Calendar Scheduling Assistant with LangChain & Groq LLM

This project implements an intelligent scheduling assistant that integrates with Google Calendar to **create, update, delete, and list events** via natural language commands. It leverages the Google Calendar API, LangChain’s *StructuredTool* agents, and Groq’s ChatGroq language model for robust conversational interactions.

---

## 🚀 Features

- **Google Calendar Integration:** Authenticate and perform CRUD operations on calendar events.
- **Natural Language Interface:** Use an LLM-powered agent to interpret user inputs for calendar management.
- **Structured Tooling:** Strongly typed function inputs with Pydantic schemas ensure accurate data handling.
- **Interactive Command Prompt:** Enter human-friendly requests that map to calendar actions.
- **Automatic Token Refresh:** Handles OAuth2 token refreshing and credential storage (`token.json`).
- **Supports Event Metadata:** Manage event title, date, time, duration, location, and description.

---
