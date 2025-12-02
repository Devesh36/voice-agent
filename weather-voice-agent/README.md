# Weather Voice Agent

A voice-based weather assistant built with LiveKit Agents that allows users to ask about weather conditions in any city using natural speech.

## Overview

This project demonstrates how to build a conversational AI agent that:
- Accepts voice input from users
- Processes weather queries using a custom tool
- Fetches real-time weather data from Open-Meteo API
- Responds with voice output
- Runs locally on your machine

The agent uses LiveKit Agents framework for voice processing, Google Gemini's Realtime API for LLM capabilities, and integrates a custom weather lookup tool.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: LiveKit Agents
- **HTTP Client**: httpx
- **Environment Management**: python-dotenv
- **External Services**:
  - LiveKit (voice transport and agent orchestration)
  - Google Gemini 2.0 Flash (LLM and voice synthesis)
  - Open-Meteo API (free weather data - no authentication required)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd weather-voice-agent
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file and fill in your API keys:
```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

#### LiveKit Credentials (Required)
- Sign up at [LiveKit Cloud](https://cloud.livekit.io/)
- Create a project and get:
  - **LIVEKIT_URL**: WebSocket URL for your LiveKit server
  - **LIVEKIT_API_KEY**: API key for server-side authentication
  - **LIVEKIT_API_SECRET**: API secret for generating client tokens

#### Google Gemini API Key (Required)
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Add it as **GOOGLE_API_KEY**

#### Weather API (Optional - Uses Free Open-Meteo)
- No setup required! Open-Meteo is completely free and requires no authentication
- The agent automatically uses Open-Meteo for weather data

Example `.env` file:
```bash
LIVEKIT_URL=wss://your-livekit-instance.livekit.cloud
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the Agent
Start the local LiveKit agent worker:
```bash
python -m src.weather_agent console
```

This command will:
- Start a LiveKit agent worker locally
- Enable voice input via your microphone
- Provide voice responses through your speakers
- Allow natural conversation about weather

## How It Works

### 1. Voice Input/Output via LiveKit
LiveKit provides real-time WebRTC communication that handles:
- Audio capture from the user's microphone
- Low-latency transmission to the agent
- Audio streaming of responses back to the user

### 2. AI Processing with Google Gemini
Google Gemini Realtime API processes the audio:
- **Speech-to-Text (STT)**: Converts voice to text automatically
- **Language Understanding**: Recognizes weather queries
- **Function Calling**: Identifies when to call the `lookup_weather` tool
- **Text-to-Speech (TTS)**: Converts AI responses back to voice

### 3. Weather Data via Open-Meteo
When a weather query is detected, the agent:
- Extracts the city name from user speech
- Calls `lookup_weather(city)` function
- Geocodes the city name to coordinates using Open-Meteo Geocoding API
- Fetches current weather data using those coordinates
- Formats the response for natural speech

### Complete Flow Example
```
User: "What's the weather in London?"
  ↓
LiveKit: Streams audio to agent
  ↓
Gemini STT: "What's the weather in London?"
  ↓
Gemini AI: Recognizes weather query, calls lookup_weather("London")
  ↓
lookup_weather():
  1. Geocode: London → (51.5085, -0.1257)
  2. Weather: (51.5085, -0.1257) → {temp: 12°C, condition: rain, humidity: 85%}
  ↓
Gemini: "In London, United Kingdom, it is 12°C with rain conditions..."
  ↓
Gemini TTS: Generates voice response
  ↓
LiveKit: Streams response back to user
  ↓
User: Hears the weather response
```

## Usage Examples

Once running, you can ask questions like:
- "What's the weather in Mumbai?"
- "Will it rain in Bangalore today?"
- "How hot is it in New York?"

The agent will respond conversationally with current temperature, conditions, humidity, and other relevant details.

## Running the React Frontend

A modern React-based frontend is available to interact with the voice agent through your browser.

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables
Copy the example environment file and add your LiveKit credentials:
```bash
cp .env.example .env
```

Edit `.env` with your actual LiveKit credentials:
- **VITE_LIVEKIT_URL**: Your LiveKit server WebSocket URL
- **VITE_LIVEKIT_TOKEN**: A valid JWT token for room access

### 3. Start the Agent Backend
In a separate terminal, start the weather agent:
```bash
python -m src.weather_agent console
```

### 4. Start the React Development Server
```bash
npm run dev
```

### 5. Open Your Browser
Navigate to the URL shown in the terminal (usually `http://localhost:5173`)

### 6. Connect and Chat
1. Click "Connect to Agent"
2. Allow microphone access when prompted
3. Start speaking - ask about weather in any city!
4. The agent will respond with voice

### Frontend Features
- **Real-time Connection Status**: Visual feedback on connection state
- **Participant Display**: Shows both you and the weather agent
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, gradient-based interface with glassmorphism effects

## Limitations & Future Work

- **Current Weather Only**: Only provides current weather data, no forecasts
- **Frontend Setup Required**: Requires manual configuration of LiveKit credentials
- **Language Support**: Primarily English, limited multilingual support
- **Error Handling**: Basic error handling for common scenarios
- **Persistence**: No conversation history or user preferences

Potential enhancements:
- Add multi-day weather forecasts
- Support for multiple languages
- User location detection
- Weather alerts and notifications
- Historical weather data
- Voice activity detection improvements
- Simplified frontend setup with environment variables