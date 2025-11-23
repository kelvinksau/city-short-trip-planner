"""
City Short Trip Planner API
---------------------------
This module defines the FastAPI application that serves as the backend for the City Short Trip Planner.
It handles user requests for trip planning, manages the agent runner session, and communicates with the
multi-agent system to generate itineraries.

Design:
- Uses FastAPI for a lightweight and fast web server.
- Integrates with Google ADK Runner to manage the agent execution lifecycle.
- Maintains a single global runner instance for simplicity in this demo context (note: production would require per-user session management).
"""

import os
import logging
import asyncio
import uuid
from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from orchester.agent import root_agent as city_short_trip_planner_agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger("city_short_trip_planner_api")
logger.setLevel(logging.INFO)

# Constants
APP_NAME = "city_short_trip_planner"
USER_ID = os.getenv("USER_ID", "user")
SESSION_ID = str(uuid.uuid4())


app = FastAPI()
runner: Runner = None

class TripRequest(BaseModel):
    """
    Data model for the trip planning request.
    """
    location: str
    interests: List[str]
    duration_days: float
    avoid: Optional[List[str]] = []

@app.on_event("startup")
async def init_runner():
    """
    Initialize the ADK Runner on application startup.
    
    This function sets up the InMemorySessionService and initializes the Runner
    with the root agent (city_short_trip_planner_agent).
    """
    global runner
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    runner = Runner(
        agent=city_short_trip_planner_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    logger.info("Runner initialized and session created.")

@app.post("/plan")
async def plan_trip(request: TripRequest):
    """
    Handle the trip planning request.

    This endpoint receives the user's trip preferences, constructs a prompt,
    and sends it to the agent runner. It then streams the response from the agent
    and returns the final itinerary.

    Args:
        request (TripRequest): The user's trip details (location, interests, duration, avoid).

    Returns:
        dict: A dictionary containing the generated itinerary in Markdown format.
    """
    global runner
    
    # Construct the user prompt from the request data
    user_input = (
        f"I will be in {request.location} for {request.duration_days} days. "
        f"I'm interested in {', '.join(request.interests)}. "
        f"Please avoid: {', '.join(request.avoid or [])}."
    )
    logger.info(f"User input: {user_input}")
    content = Content(role="user", parts=[Part(text=user_input)])

    response_text = ""
    # Run the agent asynchronously and process events
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        # We are interested in the final response from the agent
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text += event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break
            
    logger.info("System response: {response_text}")
    return {"itinerary": response_text}