import json

from shadowauth.database.postgres_repository import PostgresRepository
from shadowauth.parsers.cowrie_parser import CowrieParser


class SessionImporter:

    def __init__(self):

        self.parser = CowrieParser()

        self.repository = PostgresRepository()

    def import_file(
        self,
        file_path: str,
    ) -> None:

        with open(file_path) as file:

            for line in file:

                raw_event = json.loads(line)

                event = self.parser.parse(raw_event)

                self.repository.save_event(event)