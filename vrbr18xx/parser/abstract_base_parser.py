from abc import ABC, abstractmethod

from vrbr18xx.parser.abstract_base_pattern import Pattern18xx


class Parser18xx(ABC):

    def __init__(self, patterns: Pattern18xx):
        self.patterns = patterns

    @abstractmethod
    def parse(self, line: str) -> dict:
        pass

