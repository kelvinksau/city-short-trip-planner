"""
Root Agent Configuration
------------------------
This module defines the root agent for the City Short Trip Planner.
The root agent orchestrates the trip planning process by delegating tasks to specialized sub-agents:
- inspiration_agent: Finds attractions.
- activities_agent: Routes and schedules activities.
- itinerary_agent: Formats the final itinerary.

Design:
- Uses a hierarchical agent structure where the root agent coordinates the workflow.
- The instruction prompt strictly defines the sequence of tool calls to ensure a logical planning process.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from subagents.inspiration import inspiration_agent
from subagents.activities import activities_agent
from subagents.itinerary import itinerary_agent

# The instruction prompt defines the agent's persona, workflow, and rules.
# It explicitly instructs the agent to call the sub-agents in a specific order.
instruction_prompt = """
You are an expert City Short Trip Planner. Your task is to create one complete, attractive, and realistic personalized day (or multi-day) itinerary based on the user's request, preferences, travel dates, and available time.

    - Always deliver exactly one complete itinerary proposal (no multiple options, no back-and-forth).
    - Prioritize a mix of popular highlights and lesser-known local spots unless the user specifies otherwise.
    - Add practical tips (best photo spots, what to wear, reservation advice, costs if known, etc.) where relevant.
    - If the trip spans multiple days, structure the itinerary day-by-day with logical flow and rest time.

Proceed immediately by calling the appropriate tools in sequence without waiting for user approval.
"""

# Define the root agent with its tools (sub-agents)
root_agent = Agent(
    name="city_short_trip_planner",
    # name="local_explorer_assistant",
    model="gemini-2.5-flash",
    description="Coordinates discovery, routing, and itinerary composition to plan a multiple days short city trip.",
    instruction=instruction_prompt,
    tools=[
        AgentTool(agent=inspiration_agent),
        AgentTool(agent=activities_agent),
        AgentTool(agent=itinerary_agent)
    ]
)
