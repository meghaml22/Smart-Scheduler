from datetime import datetime, timedelta
from calendar_utils import get_calendar_service

# Helper: ISO to datetime
def parse_time(iso_string):
    return datetime.fromisoformat(iso_string)

# Helper: Convert time string like "before 9 AM" to check logic
def violates_exclude_times(slot_start, exclude_times):
    for rule in exclude_times:
        rule = rule.lower()
        hour = slot_start.hour
        if "before" in rule:
            threshold = int(rule.split("before")[1].strip().split()[0])
            if hour < threshold:
                return True
        elif "after" in rule:
            threshold = int(rule.split("after")[1].strip().split()[0])
            if hour > threshold:
                return True
    return False


def find_smart_slots(
    duration_minutes=30,
    start_date=None,
    end_date=None,
    exclude_days=None,
    exclude_times=None,
    latest_end=None,
    max_results=10
):
    service = get_calendar_service()

    now = datetime.utcnow()
    start = parse_time(start_date) if start_date else now
    end = parse_time(end_date) if end_date else now + timedelta(days=7)
    latest_end_dt = parse_time(latest_end) if latest_end else None

    # Get events from primary calendar
    busy_slots = []
    calendars = service.calendarList().list().execute()
    primary_calendar = calendars['items'][0]['id']

    events = service.events().list(
        calendarId=primary_calendar,
        timeMin=start.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    for event in events.get('items', []):
        s = event['start'].get('dateTime')
        e = event['end'].get('dateTime')
        if s and e:
            busy_slots.append((datetime.fromisoformat(s), datetime.fromisoformat(e)))

    # Generate candidate slots
    free_slots = []
    current = start.replace(minute=0, second=0, microsecond=0)

    while current + timedelta(minutes=duration_minutes) <= end:
        slot_end = current + timedelta(minutes=duration_minutes)

        # 1. Check overlaps
        overlap = any(bs[0] < slot_end and bs[1] > current for bs in busy_slots)

        # 2. Check deadline
        if latest_end_dt and slot_end > latest_end_dt:
            break

        # 3. Check excluded days
        weekday = current.strftime("%A")
        if exclude_days and weekday in exclude_days:
            current += timedelta(minutes=30)
            continue

        # 4. Check excluded times
        if exclude_times and violates_exclude_times(current, exclude_times):
            current += timedelta(minutes=30)
            continue

        # 5. Add slot if all checks pass
        if not overlap:
            free_slots.append((current, slot_end))
            if len(free_slots) >= max_results:
                break

        current += timedelta(minutes=30)

    return free_slots
