import json

from shadowauth.extractors.session_feature_extractor import SessionFeatureExtractor
from shadowauth.parsers.cowrie_parser import CowrieParser


events = []

parser = CowrieParser()

with open("samples/raw/cowrie/controlled-session-01.jsonl") as file:

    for line in file:
        raw_event = json.loads(line)
        events.append(parser.parse(raw_event))


extractor = SessionFeatureExtractor()

features = extractor.extract(events)

print(features)