"""
Weather Voice Agent - A conversational AI assistant for weather queries

This module implements a voice-based weather assistant using LiveKit Agents.
The agent listens to voice input, extracts weather queries, fetches real-time
weather data, and responds with natural voice output.

Key Components:
- LiveKit: Real-time voice communication via WebRTC
- Google Gemini: AI reasoning and voice synthesis
- Open-Meteo API: Free weather data provider
"""

import os
from typing import Dict, Any
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file for API credentials
load_dotenv()

from livekit.agents import (
    Agent,              # Base class for voice agents
    AgentSession,       # Manages the voice session
    JobContext,         # Context for job execution
    RunContext,         # Runtime context for tool execution
    WorkerOptions,      # Configuration for worker
    cli,                # Command-line interface
    function_tool,      # Decorator for exposing functions to AI
    ToolError,          # Custom error for tool failures
)
from livekit.plugins import google  # Google Gemini integration


class WeatherAgent(Agent):
    """
    A voice-based weather assistant agent using LiveKit Agents.
    
    This agent:
    1. Receives voice input from users via LiveKit
    2. Uses Google Gemini to understand weather queries
    3. Calls lookup_weather() to fetch real-time data
    4. Responds with natural voice output
    
    The agent is configured with instructions that tell Gemini to use
    the lookup_weather tool for weather queries.
    """

    def __init__(self):
        # Initialize with system instructions for Gemini AI
        super().__init__(
            instructions=(
                "You are a weather assistant. For any weather question, you MUST use the 'lookup_weather' tool. "
                "For current weather queries, respond ONLY with the temperature and weather condition (e.g., 'It is 25 degrees and sunny'). Keep it very brief. "
                "However, if the user explicitly asks for a forecast or prediction for future days, you can provide those details."
            ),
        )

    @function_tool
    async def lookup_weather(self, context: RunContext, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Look up current weather information for a given city using Open-Meteo API.
        
        This function is exposed to Gemini AI as a tool. When the user asks about
        weather, Gemini automatically calls this function with the extracted city name.
        
        The function performs a two-step process:
        1. Geocoding: Convert city name to coordinates using Open-Meteo Geocoding API
        2. Weather Fetch: Get current weather for those coordinates
        
        Args:
            context: Runtime context provided by LiveKit
            city: The name of the city to get weather for (e.g., "London", "Tokyo")
            units: Temperature units - 'metric' for Celsius (default), 'imperial' for Fahrenheit

        Returns:
            Dictionary containing:
            - city: City name
            - country: Country name
            - temperature: Current temperature
            - feels_like: Apparent temperature (feels like)
            - humidity: Relative humidity percentage
            - description: Human-readable weather description
            - units: Temperature unit (Celsius/Fahrenheit)
        
        Raises:
            ToolError: If city not found, API is down, or network error occurs
        """
        # Step 1: Geocoding - Convert city name to coordinates
        # Using Open-Meteo's free geocoding API (no authentication required)
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # Make geocoding API request
                geo_response = await client.get(geocoding_url)
                if geo_response.status_code != 200:
                    raise ToolError(f"Could not find location for '{city}'. Please try another city.")
                
                geo_data = geo_response.json()
                if not geo_data.get("results"):
                    raise ToolError(f"I couldn't find a city called '{city}'. Please check the spelling or try another city.")
                
                # Extract coordinates and location info from first result
                result = geo_data["results"][0]
                latitude = result["latitude"]
                longitude = result["longitude"]
                city_name = result.get("name", city)
                country = result.get("country", "")
                
                # Step 2: Weather Fetch - Get current weather AND daily forecast
                # We add 'daily' parameters to get max/min temps and weather codes for the next few days
                # We also add 'timezone=auto' to get the correct dates for the location
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,apparent_temperature,weather_code,relative_humidity_2m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&temperature_unit={'celsius' if units == 'metric' else 'fahrenheit'}"
                
                weather_response = await client.get(weather_url)
                if weather_response.status_code != 200:
                    raise ToolError("The weather service is temporarily unavailable. Please try again later.")
                
                weather_data = weather_response.json()
                current = weather_data["current"]
                daily = weather_data.get("daily", {})
                
                # WMO Weather Code Mapping
                # These codes are part of the WMO (World Meteorological Organization) standard
                # They represent all possible weather conditions (0-99)
                wmo_codes = {
                    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
                    45: "foggy", 48: "depositing rime fog",
                    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
                    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
                    71: "slight snow", 73: "moderate snow", 75: "heavy snow",
                    77: "snow grains", 80: "slight rain showers", 81: "moderate rain showers",
                    82: "violent rain showers", 85: "slight snow showers", 86: "heavy snow showers",
                    95: "thunderstorm", 96: "thunderstorm with slight hail", 99: "thunderstorm with heavy hail"
                }
                
                # Convert WMO code to human-readable description
                weather_code = int(current["weather_code"])
                description = wmo_codes.get(weather_code, "unknown conditions")
                
                # Process forecast data
                forecast = []
                if daily:
                    times = daily.get("time", [])
                    codes = daily.get("weather_code", [])
                    max_temps = daily.get("temperature_2m_max", [])
                    min_temps = daily.get("temperature_2m_min", [])
                    
                    for i in range(min(len(times), 5)):  # Get up to 5 days
                        code = int(codes[i])
                        forecast.append({
                            "date": times[i],
                            "description": wmo_codes.get(code, "unknown"),
                            "max_temp": max_temps[i],
                            "min_temp": min_temps[i]
                        })

                # Return formatted weather data as a dictionary
                return {
                    "city": city_name,
                    "country": country,
                    "temperature": current["temperature_2m"],
                    "feels_like": current["apparent_temperature"],
                    "humidity": current["relative_humidity_2m"],
                    "description": description,
                    "units": "Celsius" if units == "metric" else "Fahrenheit",
                    "forecast": forecast
                }
            except httpx.RequestError:
                # Network error - likely no internet connection
                raise ToolError("Unable to connect to the weather service. Please check your internet connection and try again.")


async def entrypoint(ctx: JobContext):
    """
    Entrypoint function for the LiveKit agent worker.
    
    This function is called when a new job is started. It:
    1. Loads environment variables (API credentials)
    2. Connects to the LiveKit room
    3. Creates a Gemini Realtime session for voice processing
    4. Initializes the weather agent
    5. Sends an initial greeting
    
    Args:
        ctx: JobContext containing room information and configuration
    """
    # Load environment variables from .env file in parent directory
    # This includes LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, GOOGLE_API_KEY
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path, override=True)

    # Connect to the LiveKit room
    await ctx.connect()

    # Create a session with Google Gemini Realtime API for voice
    # This enables:
    # - Speech-to-Text: Converts user voice to text
    # - LLM Processing: Understands user intent and calls tools
    # - Text-to-Speech: Converts response back to voice
    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            voice="Puck",  # Available voices: Puck, Breeze, Charon, Juniper, Orion
        ),
    )

    # Create an instance of our custom weather agent
    agent = WeatherAgent()

    # Start the agent session in the room
    # The agent will now listen for incoming audio and respond
    await session.start(agent=agent, room=ctx.room)

    # Send initial greeting message to the user
    await session.generate_reply(
        instructions="Hi, I'm your weather assistant. Ask me about the weather in any city."
    )


# Entry point for the CLI
# This allows running the agent with: python src/weather_agent.py dev


# Entry point for the CLI
# This allows running the agent with: python src/weather_agent.py dev

if __name__ == "__main__":
    # Run the app as a LiveKit worker
    # The CLI handles parsing arguments (dev, start, etc.)
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))