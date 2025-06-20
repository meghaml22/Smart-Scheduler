# 🧠 Smart Voice Scheduler

Smart Voice Scheduler is a voice-enabled calendar agent built with **FastAPI**, **Google Gemini (Generative AI)**, and **Google Calendar API**. The assistant listens to scheduling requests like:

> “Book a meeting for next Friday from 4:30 to 5:30 with HR”

It intelligently understands your request, checks your availability, and books a meeting on your Google Calendar — all automatically.

---

## 🚀 How to Set Up and Run the Project

1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-voice-scheduler.git
cd smart-voice-scheduler
2. Create a Python Virtual Environment and Install Dependencies
bash
Copy
Edit
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
If you don’t have requirements.txt, install manually:

bash
Copy
Edit
pip install fastapi uvicorn python-dotenv google-api-python-client google-auth google-auth-oauthlib
3. Set Up Environment Variables
Create a .env file in the root directory and add your Gemini API key:

ini
Copy
Edit
GEMINI_API_KEY=your_gemini_api_key
You can get this key from Google AI Studio.

4. Configure Google Calendar API
Go to Google Cloud Console

Enable Google Calendar API

Create OAuth 2.0 Client ID credentials (Desktop App)

Download credentials.json and place it in your project root

5. Authorize Access to Your Calendar
Run this command once to log in and generate token.pickle:

bash
Copy
Edit
python -c "from calendar_utils import get_calendar_service; get_calendar_service()"
6. Start the Server
bash
Copy
Edit
uvicorn main:app --reload --port 8000
7. (Optional) Expose Locally with ngrok
bash
Copy
Edit
ngrok http 8000
Use the public URL in a service like Vapi.ai to send voice input to the agent.

🧠 How It Works
Voice Input
You speak or send a request like:

“Schedule a 30-minute meeting on Friday at 4 PM”

Agent Pipeline
Transcription: (Handled by Vapi or UI)

Gemini AI: Extracts structured intent like:

json
Copy
Edit
{
  "duration": 60,
  "preferred_day": "Friday",
  "start_time": "2025-06-28T16:30:00",
  "end_time": "2025-06-28T17:30:00",
  "title": "Meeting with HR"
}
FastAPI Backend:

Uses find_free_slots() to check availability

Calls create_event() to book on your calendar

Final Reply:

“✅ Meeting booked for Friday at 4:30 PM. Check your calendar!”

🧩 Design Choices
Stateless Gemini prompts for structured data extraction only (no memory or long conversations)

FastAPI for clean and fast webhook-style interaction

Google Calendar API used with full read/write OAuth2 flow

Modular design for easy integration with voice frontends like Vapi.ai or Whisper
