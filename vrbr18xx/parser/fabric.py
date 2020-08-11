from vrbr18xx.parser.abstract_base_parser import Parser18xx
from vrbr18xx.parser.abstract_base_pattern import Pattern18xx
from vrbr18xx.parser.patterns_1846 import Patterns1846
from vrbr18xx.parser.dummy_parser import DummyParser
from vrbr18xx.parser.parser_1846 import Parser1846


def create_parser(game: str) -> Parser18xx:
    if game == '1846':
        return Parser1846(Patterns1846())
    if game == 'Dummy':
        return DummyParser()
    raise NotImplementedError('The parser of this game is not implemented')


def create_pattern(game: str) -> Pattern18xx:
    if game == '1846':
        return Patterns1846()
    raise NotImplementedError('The pattern of this game is not implemented')