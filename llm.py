from dotenv import load_dotenv
import os
from langchain.agents import Tool
from function import create_event, update_event, delete_event
from langchain.agents import AgentType, initialize_agent
from typing import Optional
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from langchain.schema import SystemMessage
import pytz
import calendar
from datetime import datetime, timedelta
from langchain_groq import ChatGroq

# Load environment variables before using them
load_dotenv()

# Initialize the Groq LLM
llm = ChatGroq(
    model="qwen-qwq-32b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

# --------------------- Input Schemas ---------------------
class DeleteEventParameters(BaseModel):
    event_name: str = Field(description="name of the event to be deleted")

class UpdateEventParameters(BaseModel):
    event_name: str = Field(description="name of the event to be updated")
    date: Optional[str] = Field(description="updated start date of the event (YYYY-MM-DD)")
    time: Optional[str] = Field(description="updated start time of the event (HH:MM)")
    duration: Optional[int] = Field(description="updated duration in hours")
    name: Optional[str] = Field(description="updated title of the event")
    description: Optional[str] = Field(description="updated description of the event")
    location: Optional[str] = Field(description="updated location of the event")

class CreateEventParameters(BaseModel):
    date: str = Field(description="start date of the event (YYYY-MM-DD)")
    time: str = Field(description="start time of the event (HH:MM)")
    name: str = Field(description="name or title of the event")
    duration: int = Field(1, description="duration of the event in hours (default: 1)")
    description: Optional[str] = Field(None, description="description of the event")
    location: Optional[str] = Field(None, description="location of the event")

# --------------------- User Input ---------------------
query = input("Enter details: ")

if query and len(query.strip()) > 0:
    # Define tools
    tools = [
        StructuredTool.from_function(
            name="Create Event",
            func=create_event,
            description="Create an event in Google Calendar",
            args_schema=CreateEventParameters,
        ),
        StructuredTool.from_function(
            name="Update Event",
            func=update_event,
            description="Update an event in Google Calendar",
            args_schema=UpdateEventParameters,
        ),
        StructuredTool.from_function(
            name="Delete Event",
            func=delete_event,
            description="Delete an event from Google Calendar",
            args_schema=DeleteEventParameters,
        ),
    ]

    system_message = SystemMessage(
        content="You are a helpful and accurate scheduling assistant. "
                "Only create, update, or delete events one at a time. "
                "Use only the provided fields; do not assume details like location or description if not given."
                "Use the tools given for creating, updating, or deleting events in the google calendar."
    )

    def get_prefix(current_time):
        timezone = pytz.timezone("UTC")
        tomorrow_date = current_time + timedelta(days=1)
        current_year = current_time.year

        return f"""
        Current UTC time: {current_time}
        ISO format: {current_time.astimezone(timezone).isoformat()}
        Tomorrow (ISO): {tomorrow_date.isoformat()}
        Day of the week: {calendar.day_name[current_time.astimezone(timezone).weekday()]}
        Current year: {current_year}
        Note: Only perform one action per request. Do not assume missing values.
        """

    current_time = datetime.now(pytz.timezone("UTC"))
    prefix_message = get_prefix(current_time)

    # Initialize agent
    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={
            "system_message": system_message,
            "prefix": prefix_message,
        },
    )

    response = agent_chain.run(input=query)
    print(response)
else:
    print("Error: Empty input or unable to parse parameters.")
