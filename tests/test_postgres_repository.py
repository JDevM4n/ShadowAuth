import json

from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.parsers.cowrie_parser import CowrieParser

repository = PostgresRepository()
parser = CowrieParser()

with open("samples/raw/cowrie/controlled-session-01.jsonl") as file:
    raw_event = json.loads(file.readline())

event = parser.parse(raw_event)

repository.save_event(event)

events = repository.get_session(event.session_id)

print(f"Recovered {len(events)} events")

for event in events:

    print(event.event_id)