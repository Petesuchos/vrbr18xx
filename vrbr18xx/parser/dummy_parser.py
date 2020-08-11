from vrbr18xx.parser.abstract_base_parser import Parser18xx


class DummyParser(Parser18xx):

    def __init__(self, pattern=None):
        pass

    def parse(self, line: str) -> dict:
        return dict(action='dummy action')
