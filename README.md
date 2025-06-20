# 📅 Smart Voice Scheduler

This is a voice-enabled assistant that helps schedule meetings on your **Google Calendar** using **FastAPI** and **Gemini (Google Generative AI)**.

You can say things like:

> “Book a meeting for next Friday from 4:30 to 5:30 with HR”

And it will:
- Understand your request
- Find free time on your calendar
- Create the event automatically
- Reply with confirmation

---

## 🛠 Requirements

- Python 3.9+
- Google Calendar API credentials
- Gemini API key

---

## 🔧 Setup

1. **Clone the repo**  
2. Add your `.env` file with:
    ```
    GEMINI_API_KEY=your-gemini-api-key
    ```

3. Add your `credentials.json` from Google Cloud to the project root  
4. Run once to authenticate and generate `token.pickle`:
    ```bash
    python -c "from calendar_utils import get_calendar_service; get_calendar_service()"
    ```

5. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Start the app:
    ```bash
    uvicorn main:app --reload
    ```

---

## 🔗 Usage

Connect this to a voice frontend (like Vapi.ai or Whisper) or test it by sending a POST request to:

