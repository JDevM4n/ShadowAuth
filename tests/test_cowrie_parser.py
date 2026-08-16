from datetime import datetime

from shadowauth.parsers.cowrie_parser import CowrieParser

parser = CowrieParser()

raw_event = {
    "eventid": "cowrie.session.connect",
    "timestamp": datetime.now(),
    "session": "abc123"
}

normalized = parser.parse(raw_event)

print(normalized)