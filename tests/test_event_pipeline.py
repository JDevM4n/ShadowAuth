import json

from shadowauth.collectors.event_collector import EventCollector
from shadowauth.parsers.cowrie_parser import CowrieParser
from shadowauth.pipeline.event_pipeline import EventPipeline


with open("samples/raw/controlled-session-01.jsonl") as file:
    raw_event = json.loads(file.readline())

parser = CowrieParser()

collector = EventCollector()

pipeline = EventPipeline(parser, collector)

pipeline.process(raw_event)