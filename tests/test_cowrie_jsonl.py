# Este codigo 

import json

from shadowauth.parsers.cowrie_parser import CowrieParser

parser = CowrieParser()

with open(
    "samples/raw/controlled-session-01.jsonl",
    "r",
    encoding="utf-8"
) as file:

    first_line = file.readline()

raw_event = json.loads(first_line)

normalized = parser.parse(raw_event)

print(normalized)