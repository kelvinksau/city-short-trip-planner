"""
Activities Agent
----------------
This module defines the `activities_agent`, which is responsible for planning the logistics of the trip.
It determines the best route, timing, and transportation options between selected locations.

Design:
- Specialized agent focused on routing and scheduling.
- Uses `google_search` to fetch real-time transport and location data.
- Instructions emphasize practical, real-world routing (e.g., walking vs. public transport).
"""

import logging

from google.adk.agents import Agent
from google.adk.tools import google_search
#from google.adk.tools import google_maps_grounding

# Configure logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

instruction_prompt = """
You are an intelligent routing agent tasked with finding the best practical route from a starting point to a destination, optionally passing through specified waypoints.

Preferences:
- Prioritize walking routes whenever they are reasonable in terms of distance and time.
- If walking is impractical (too long, unsafe, or not feasible), suggest the fastest or most convenient local public transportation options (bus, MRT/LRT, tram, ferry, etc.) or a combination of walking + public transport.
- Always consider real-world conditions in Singapore where applicable (e.g., frequent sheltered walkways, heat, rain, peak hours).

Capabilities:
- You have access to the google_search tool. Use it as many times as needed to retrieve up-to-date Google Maps directions, transit schedules, walking times, or any relevant transport information.
- When using the tool, craft clear and specific queries (e.g., "Google Maps walking directions from Jurong East MRT to IMM Singapore", "bus from Orchard Road to Bugis timing Singapore", "fastest way from Changi Airport Terminal 3 to Marina Bay Sands").

Response format:
- Provide a clear, step-by-step route.
- Include estimated travel time and distance for each leg.
- Mention the total estimated duration and preferred mode(s).
- Highlight any transfers, walking segments, or important notes (e.g., "take sheltered walkway", "last bus at 23:30").
- If multiple good options exist, list the top 2–3 with pros/cons.

Always verify information with current search results before finalizing your answer.
"""

activities_agent = Agent(
    name="activities_agent",
    model="gemini-2.5-flash",
    description=(
        "Estimates an optimal activities plan using ADK v1.15+ google_search tool."
    ),
    tools=[google_search]
)

