from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from calendar_utils import find_free_slots, create_event
from gemini_engine import extract_with_constraints
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Smart Scheduler API is live!"}

def pick_matching_slot(slots, preferred_day, time_range):
    for s, e in slots:
        if preferred_day.lower() in s.strftime("%A").lower():
            if time_range == "morning" and s.hour < 12:
                return (s, e)
            elif time_range == "afternoon" and 12 <= s.hour < 17:
                return (s, e)
            elif time_range == "any":
                return (s, e)
    return None

@app.post("/vapi-webhook")
async def vapi_webhook(request: Request):
    data = await request.json()
    user_text = data.get("payload", {}).get("transcript", "")
    if not user_text:
        return JSONResponse({"text": "Sorry, I didn’t catch that."})

    parsed = extract_with_constraints(user_text)

    if not parsed.get("duration") or not parsed.get("preferred_day") or not parsed.get("time_range"):
        return JSONResponse({"text": "Please tell me the duration, day, and time for the meeting."})

    slots = find_free_slots(duration_minutes=parsed["duration"])
    slot = pick_matching_slot(slots, parsed["preferred_day"], parsed["time_range"])

    if not slot:
        return JSONResponse({"text": f"Sorry, I couldn't find any free slots on {parsed['preferred_day']}. Try another day?"})

    start_time = slot[0]
    end_time = slot[1]

    event_link = create_event(
        summary="Meeting via Voice Assistant",
        start_time=start_time,
        end_time=end_time
    )

    return JSONResponse({
        "text": f"✅ Your {parsed['duration']} minute meeting has been scheduled for {start_time.strftime('%A at %I:%M %p')}. [Calendar Event]({event_link})"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
