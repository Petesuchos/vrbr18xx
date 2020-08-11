from unittest import TestCase
from vrbr18xx.parser.fabric import create_parser


class TestParser(TestCase):

    def test_create_parser(self):
        parser = create_parser(game='Dummy')
        self.assertDictEqual({'action': 'dummy action'}, parser.parse('Parse this'))

    def test_create_parser_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            create_parser(game='BAD PARSER')

