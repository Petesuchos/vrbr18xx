from unittest import TestCase, skip
from vrbr18xx.parser.fabric import create_parser


class TestParser1846(TestCase):
    def setUp(self):
        self.parser = create_parser('1846')



    def test_introduce_player(self):
        lines = dict(
            Petesuchos='Petesuchos chooses a company',
            Burgos='Burgos chooses a company',
            Rivaben='Rivaben chooses a company',
            ftola='ftola chooses a company'
        )

        for player_name, line in lines.items():
            self.assertDictEqual({'action': 'introduce_player', 'player': player_name}, self.parser.parse(line))

