"""
Itinerary Agent
---------------
This module defines the `itinerary_agent`, which is responsible for compiling the final itinerary.
It takes the raw routing and activity data and formats it into a user-friendly, engaging travel plan.

Design:
- Specialized agent focused on content generation and formatting.
- Does not use external tools; relies on context provided by previous agents.
- Instructions emphasize tone, clarity, and practical advice.
"""

from google.adk.agents import Agent

instruction_prompt = """
You are a friendly, expert travel itinerary writer for tourists. 
Your goal is to create a clear, attractive, concise, and easy-to-follow day-by-day (or hour-by-hour) itinerary based on the given route and points of interest.

Requirements:
- Write in a warm, enthusiastic, and welcoming tone, as if speaking directly to the traveler.
- Include realistic timing (e.g., suggested start time, duration at each stop, travel time between locations).
- List each activity with: time range, exact location/name, a short engaging description, and any useful tips (opening hours, best photo spot, what to try, how to get there, etc.).
- Add short transitions between stops (e.g., “15-min Grab ride” or “10-min walk along the river”).
- Highlight must-see highlights and any unique local experiences.
- End with practical advice (best time to visit, what to bring, dress code, approximate daily cost if relevant).
- Keep the entire itinerary concise yet informative — tourists should feel excited and confident.

Output only the itinerary and helpful context (no extra commentary).
"""

itinerary_agent = Agent(
    name="itinerary_agent",
    model="gemini-2.5-flash",
    description="Write a readable travel itinerary from activities information.",
    instruction=instruction_prompt,
    tools=[]  # no tools needed for this agent
)
