from graduate_imitator.apps.graduation.infrastructure.parsers.presentation_parser.presentation_parser import PresentationParser


class PresentationProcessingService:
    def process_presentation(self, presentation):
        presentation_data = PresentationParser.parsePPTX(presentation)

