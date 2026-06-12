# IELTS Speaking Partner

A simplified, low-latency, and real-time audio conversation application built to help you practice and improve your English for the IELTS speaking exam. The app utilizes Google's **Gemini Multimodal Live API** (via WebSockets) to simulate a strict, realistic speaking partner.

## Key Features

- **Gemini Live Connection**: Connects to `models/gemini-3.1-flash-live-preview` (with fallback choices for Gemini 2.0 Live and Gemini 2.5 Flash) for instantaneous, bidirectional voice conversations.
- **Strict Evaluator Persona**: Configured with a system prompt instructing the AI to act as a realistic examiner checking for mistakes in vocabulary and grammar at IELTS Band 6.0–7.0.
- **Audio Gate (Volume Threshold)**: Automatically filters out background room noise and static when you are silent by skipping transmission of audio frames below `0.015` RMS.
- **Barge-in / Interruptions**: Your microphone streams continuously when the session is active, allowing you to interrupt the AI naturally by speaking.
- **Real-Time Corrections Log**: Displays a text transcription of the AI's feedback so you can read its corrections.
- **Safe configuration**: No API keys are stored in the source code or uploaded to GitHub.

---

## Setup & Running the Project

### Prerequisite
You need a **Gemini API Key** from Google AI Studio.

### 1. Configuration
Open the `.env` file in the project root and add your key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 2. Launching the App (Windows Shortcut)
Simply double-click the **`run_ielts_practice.bat`** file in the root directory. This script will:
1. Start the FastAPI backend server on `http://127.0.0.1:8000`
2. Start the Vite React frontend on `http://localhost:5173`
3. Open your default web browser automatically at `http://localhost:5173`

### 3. Manual Launching

**FastAPI Backend:**
```bash
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

**React Frontend:**
```bash
cd ielts-app
npm install
npm run dev
```

---

## Quota Limit Troubleshooting
If you encounter a `Resource has been exhausted (e.g. check quota)` error:
- Google's Live API free tier restricts keys to **1 concurrent WebSocket connection**. Wait 1-2 minutes for Google's server to drop the old connection and refresh.
- Try selecting a different model option (like `Gemini 2.0 Live (Experimental)` or `Gemini 2.5 Flash`) in the Practice Configuration dropdown before starting.
