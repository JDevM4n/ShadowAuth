from datetime import datetime

from shadowauth.models.normalized_event import NormalizedEvent


event = NormalizedEvent(
    event_id="123",
    source="cowrie",
    event_type="session.connect",
    event_timestamp=datetime.now()
)

print(event)