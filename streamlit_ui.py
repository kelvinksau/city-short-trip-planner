"""
City Short Trip Planner UI
--------------------------
This module defines the Streamlit user interface for the City Short Trip Planner.
It provides a form for users to input their trip preferences and displays the generated itinerary.

Design:
- Uses Streamlit for rapid UI development.
- Communicates with the backend FastAPI service via HTTP requests.
- Handles user input validation and displays loading states.
- Modernized layout with sidebar inputs and custom styling.
"""

import streamlit as st
import requests
import json

API_URL = "http://localhost:8000/plan"  # Adjust if FastAPI runs elsewhere

# Configure the Streamlit page
st.set_page_config(
    page_title='City Short Trip Planner',
    page_icon="images/gemini_avatar.png",
    layout="wide",
    initial_sidebar_state='expanded'
)

# Custom CSS for a cleaner, modern look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #333;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for Inputs
with st.sidebar:
    st.image("images/gemini_avatar.png", width=50)
    st.title("Trip Settings")
    st.markdown("Customize your perfect getaway.")
    
    with st.form("trip_form"):
        location = st.text_input("🌍 City Destination", value="Singapore", help="Where do you want to go?")
        
        interests = st.text_area(
            "❤️ Interests", 
            value="culture, food, history, nature", 
            help="What do you love? (comma-separated)",
            height=100
        )
        
        duration = st.slider(
            "⏳ Duration (Days)", 
            min_value=1, 
            max_value=7, 
            value=3,
            help="How long is your trip?"
        )
        
        avoid = st.text_input(
            "🚫 Avoid", 
            value="crowds, tourist traps", 
            help="Anything you dislike? (comma-separated)"
        )
        
        st.markdown("---")
        submitted = st.form_submit_button("✨ Plan My Trip")

# Main Content Area
st.title("✈️ City Short Trip Planner")
st.markdown(
    """
    <div style='background-color: #e1f5fe; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <p style='margin:0; color: #0277bd; font-size: 1.1em;'>
            Welcome! I'm your AI travel assistant. Tell me where you want to go in the sidebar, 
            and I'll craft a personalized itinerary just for you.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

if submitted:
    if not location:
        st.error("Please enter a destination city.")
    else:
        # Create a placeholder for the result
        result_container = st.container()
        
        with st.status("🤖 AI Agent is working...", expanded=True) as status:
            st.write("🔍 Analyzing your preferences...")
            
            try:
                # Prepare the payload for the API request
                payload = {
                    "location": location,
                    "interests": [i.strip() for i in interests.split(",") if i.strip()],
                    "duration_days": float(duration),
                    "avoid": [a.strip() for a in avoid.split(",") if a.strip()] if avoid else []
                }
                
                st.write("💡 Finding the best spots...")
                # Send the request to the backend API
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    itinerary = response.json().get("itinerary", "No response from agent.")
                    
                    st.write("📝 Formatting your itinerary...")
                    status.update(label="✅ Trip Planned!", state="complete", expanded=False)
                    
                    with result_container:
                        st.markdown("## 🗺️ Your Itinerary")
                        st.markdown("---")
                        st.markdown(itinerary, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        # Download Button
                        st.download_button(
                            label="📥 Download Itinerary",
                            data=itinerary,
                            file_name=f"trip_to_{location.replace(' ', '_').lower()}.md",
                            mime="text/markdown"
                        )
                else:
                    status.update(label="❌ Error", state="error")
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                status.update(label="❌ Connection Failed", state="error")
                st.error(f"Request failed: {e}")
                st.info("Make sure the FastAPI backend is running on http://localhost:8000")