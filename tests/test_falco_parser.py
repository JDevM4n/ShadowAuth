import json

from shadowauth.parsers.falco_parser import FalcoParser


with open("samples/raw/falco/falco-session-01.jsonl") as file:
    raw_event = json.load(file)

parser = FalcoParser()

event = parser.parse(raw_event)

print(event)