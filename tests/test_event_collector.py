import json

from shadowauth.collectors.event_collector import EventCollector
from shadowauth.parsers.cowrie_parser import CowrieParser


with open("samples/raw/cowrie/controlled-session-01.jsonl") as file:

    first_line = file.readline()

raw_event = json.loads(first_line)

parser = CowrieParser()

normalized_event = parser.parse(raw_event)

collector = EventCollector()

collector.collect(normalized_event)