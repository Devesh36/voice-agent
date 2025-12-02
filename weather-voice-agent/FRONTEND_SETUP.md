# 🚀 Quick Start - Weather Voice Agent

## One-Time Setup

### 1. Install Frontend Dependencies

```bash
cd frontend
npm install
```

This will download all required packages.

### 2. Make Sure Parent .env is Configured

Check `/Users/deveshrathod/Dev/internship-ai/voice-ai/weather-voice-agent/.env` has:

```env
LIVEKIT_URL=wss://voice-assisantant-71kx5unc.livekit.cloud
LIVEKIT_API_KEY=APIyf4LqDtKDGfn
LIVEKIT_API_SECRET=sBFigelqDbJebFY2crsJvfCWIRD3ugWj1eSZNyf1QTNE
GOOGLE_API_KEY=AIzaSyDtA8KpsHvIB5fgtvnNi52RKnlo7ZnqWYk
```

## Running the Project

### Terminal 1: Start Python Agent

```bash
cd /Users/deveshrathod/Dev/internship-ai/voice-ai/weather-voice-agent
/Users/deveshrathod/Dev/internship-ai/.venv/bin/python src/weather_agent.py dev
```

Wait for output:
```
DEV    livekit.agents   Watching /path/to/src
```

### Terminal 2: Start Frontend + Server

```bash
cd /Users/deveshrathod/Dev/internship-ai/voice-ai/weather-voice-agent/frontend
npm run start
```

This starts both:
- Express server on port 3000 (token generation)
- Serves React frontend

### Terminal 3 (Optional): Start Vite Dev Server

For hot reload during development:

```bash
cd /Users/deveshrathod/Dev/internship-ai/voice-ai/weather-voice-agent/frontend
npm run dev
```

Frontend will be at http://localhost:5173

## Usage

1. Open browser to `http://localhost:3000`
2. Allow microphone access when prompted
3. Click the microphone button
4. Ask about weather: "What's the weather in London?"
5. Listen to the agent respond with voice

## Demo Queries to Try

- "What's the weather in Mumbai?"
- "How about Tokyo?"
- "Tell me about weather in New York"
- "Is it raining in London?"

## Architecture

```
┌─────────────────────────────────────────────┐
│ Browser (http://localhost:3000)             │
│ - React UI                                  │
│ - Microphone input                          │
│ - Speaker output                            │
└─────────────────────────────────────────────┘
        ↕ WebRTC
┌─────────────────────────────────────────────┐
│ LiveKit Server (Cloud)                      │
│ - Audio routing                             │
│ - Room management                           │
└─────────────────────────────────────────────┘
        ↕
┌─────────────────────────────────────────────┐
│ Python Weather Agent (Port 8081)            │
│ - Listens to audio                          │
│ - Gemini AI processing                      │
│ - Weather API calls                         │
│ - Voice responses                           │
└─────────────────────────────────────────────┘
```

## Troubleshooting

**Issue: Can't connect to agent**
- Check Python agent is running (Terminal 1)
- Verify LiveKit credentials in .env

**Issue: Microphone not working**
- Check browser microphone permissions
- Try a different browser
- Verify system microphone works

**Issue: npm install fails**
- Delete `node_modules` folder
- Run `npm install` again
- Check Node.js version (14+ required)

## File Structure

```
weather-voice-agent/
├── src/
│   └── weather_agent.py          # Python agent
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # React component
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Styles
│   ├── server.js                 # Express server
│   ├── package.json              # Dependencies
│   ├── vite.config.js            # Vite config
│   └── index.html                # HTML template
├── .env                          # Credentials
└── README.md                     # Full docs
```

## Next Steps

1. ✅ Setup complete - agent and frontend running
2. 🎥 Record a demo video showing voice interaction
3. 📤 Submit to assignment

Happy building! 🚀
