import streamlit as st
from voice_stt import transcribe_audio
from voice_tts import speak_text
from gemini_engine import extract_meeting_details
from smarter_slot_filter import find_smart_slots
from calendar_utils import create_event
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="🎙️ Voice AI Scheduler", layout="centered")
st.title("🧠 Smart Voice Scheduler with Audio")

st.markdown("Upload a `.wav` audio file of your request, and I'll try to schedule it for you.")

# 1. Upload Audio
uploaded_file = st.file_uploader("Upload voice (.wav only)", type=["wav"])

if uploaded_file is not None:
    with open("audio.wav", "wb") as f:
        f.write(uploaded_file.read())

    st.audio("audio.wav", format="audio/wav")
    st.success("✅ Audio uploaded successfully.")

    # 2. Transcribe
    with st.spinner("🎤 Transcribing with Whisper..."):
        user_text = transcribe_audio("audio.wav")
    st.markdown(f"**🧑 You said:** `{user_text}`")

    # 3. Parse with Gemini
    with st.spinner("🤖 Understanding request..."):
        parsed = extract_meeting_details(user_text)
    st.subheader("🧠 Parsed Details")
    st.json(parsed)

    # 4. Fallback UI if missing fields
    if not parsed.get("duration"):
        parsed["duration"] = st.slider("Select duration (minutes):", 15, 120, 30)
    if not parsed.get("preferred_day"):
        parsed["preferred_day"] = st.selectbox("Choose a day:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    if not parsed.get("time_range"):
        parsed["time_range"] = st.radio("Choose time preference:", ["morning", "afternoon"])

    st.success("✅ Looking for available slots...")

    # 5. Time Range Mapping
    today = datetime.today()
    preferred_day = parsed["preferred_day"].lower()
    if preferred_day == "tomorrow":
        target_date = today + timedelta(days=1)
    else:
        weekday_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2,
            "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
        }
        target_date = today + timedelta((weekday_map.get(preferred_day, 0) - today.weekday()) % 7)

    start_date = target_date.replace(hour=0, minute=0).isoformat()
    end_date = (target_date + timedelta(days=1)).isoformat()

    # 6. Find Smart Slots
    slots = find_smart_slots(
        duration_minutes=parsed["duration"],
        start_date=start_date,
        end_date=end_date,
        exclude_days=parsed.get("exclude_days", []),
        exclude_times=parsed.get("exclude_times", [])
    )

    # 7. Show Results
    if slots:
        st.subheader("📅 Available Time Slots")
        slot_labels = [f"{s.strftime('%A %I:%M %p')} - {e.strftime('%I:%M %p')}" for s, e in slots]
        selected = st.selectbox("Choose a slot to confirm:", slot_labels)

        if st.button("✅ Confirm Meeting"):
            idx = slot_labels.index(selected)
            start, end = slots[idx]
            event_link = create_event("Smart Scheduled Meeting", start, end)
            st.success("✅ Meeting scheduled successfully!")
            st.markdown(f"🔗 [View in Google Calendar]({event_link})")
            speak_text("Your meeting has been scheduled. Check your calendar.")
    else:
        st.error("❌ No available time slots found. Try changing the inputs.")
