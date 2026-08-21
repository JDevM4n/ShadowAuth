from shadowauth.collectors.event_collector import EventCollector
from shadowauth.models.normalized_event import NormalizedEvent
from shadowauth.parsers.base_parser import BaseParser


class EventPipeline:
    """
    Coordinates the event processing workflow.

    The pipeline is responsible for orchestrating the different
    components involved in processing an event.
    """

    def __init__(
        self,
        parser: BaseParser,
        collector: EventCollector
    ):

        self.parser = parser
        self.collector = collector

    def process(self, raw_event: dict) -> NormalizedEvent:
        """
        Process a raw event through the pipeline.
        """

        normalized_event = self.parser.parse(raw_event)

        self.collector.collect(normalized_event)

        return normalized_event