# How to Run the Weather Voice Agent Demo

To record your demo video, you need to run three separate processes in three terminal windows.

## Prerequisites
- Ensure you are in the `voice-ai/weather-voice-agent` directory.
- Ensure you have run `npm install` in the `frontend` directory (which we just fixed).

## Step 1: Start the Token Server (Terminal 1)
This server generates security tokens for the frontend to connect to LiveKit.

```bash
cd frontend
npm run server
```
*You should see: "✅ Server running on: http://localhost:3000"*

## Step 2: Start the Frontend UI (Terminal 2)
This is the React website you will interact with.

```bash
cd frontend
npm run dev
```
*You should see: "➜ Local: http://localhost:3001/"*
*Open this URL in your browser.*

## Step 3: Start the Python AI Agent (Terminal 3)
This is the "brain" that listens to you and speaks back.

```bash
# Make sure your virtual environment is activated if you use one
# source venv/bin/activate

python src/weather_agent.py dev
```
*You should see: "Agent connected to room: weather-room"*

## Step 4: Use the App
1. Go to `http://localhost:3001` in your browser.
2. Click "Connect".
3. Allow microphone access.
4. Say "Hello" or ask "What is the weather in London?".
5. The AI should respond!

## Troubleshooting
- If you see "Failed to get token", make sure the **Token Server** (Step 1) is running.
- If you connect but the AI doesn't answer, make sure the **Python Agent** (Step 3) is running.
