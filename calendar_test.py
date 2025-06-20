from calendar_utils import find_free_slots

slots = find_free_slots(60)
for start, end in slots:
    print(f"Available: {start.strftime('%A %I:%M %p')} - {end.strftime('%I:%M %p')}")
