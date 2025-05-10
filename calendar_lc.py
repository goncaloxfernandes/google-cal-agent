import os

from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)

from langchain_google_community import CalendarToolkit
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from googleapiclient.discovery import build
import google.auth

agent = None

def init_lc():
    print("Initializing agent.")
    global agent

    credentials, project = google.auth.default(
        scopes=["https://www.googleapis.com/auth/calendar"]
    )

    # Build the Google Calendar API service using the obtained credentials
    api_resource = build("calendar", "v3", credentials=credentials)

    calendar_toolkit = CalendarToolkit(api_resource=api_resource)

    # Initialize your chat model (assuming you have a function for this)
    model = init_chat_model('gemini-2.0-flash', model_provider="google_genai")

    agent = create_react_agent(model, calendar_toolkit.get_tools(), prompt="You are a calendar assistant that helps me manage the events I have, use the tools necessary to answer the prompts. Don't ask additional questions, just do the best you can with the information you receive. Explain the end result at the end, such as assumptions you made, etc.")

def execute_query(query: str):
    query = query + ".Use whatever tools necessary to achieve this."
    print(f"Executing query: {query}")

    events = agent.stream(
        {"messages": [("user", query)]},
        stream_mode='values',
    )   

    for event in events:
        event['messages'][-1].pretty_print()
