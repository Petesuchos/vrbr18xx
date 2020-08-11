import re
from unittest import TestCase
from vrbr18xx.parser.abstract_base_pattern import Pattern18xx
from vrbr18xx.parser.fabric import create_pattern

class TestPatterns1846(TestCase):

    def setUp(self):
        self.pattern = create_pattern(game='1846')

    def test_pt_private_companies(self):
        valid_companies = [
            "Steamboat Company",
            "Meat Packing Company",
            "Michigan Central",
            "Mail Contract",
            "Michigan Southern",
            "Ohio & Indiana",
            "Lake Shore Line",
            "Tunnel Blasting Company",
            "Big 4",
            "Chicago and Western Indiana"
        ]

        invalid_companies = [
            "StReamboat Company",
            "Neat Packing Company",
            "Mixigan Central",
            "Mail",
            "Highlander",
        ]

        for valid_company in valid_companies:
            self.assertRegex(valid_company, self.pattern.private_companies())

        for invalid_company in invalid_companies:
            self.assertNotRegex(invalid_company, self.pattern.private_companies())

    def test_pt_railroads(self):
        valid_rr = [
            "PRR",
            "NYC",
            "B&O",
            "C&O",
            "ERIE",
            "GT",
            "IC"
        ]

        invalid_rr = [
            "AK",
            "NIC",
            "B&&O",
            "X&O",
            "PETRO",
            "",
            "N Y C"
        ]

        for rr in valid_rr:
            self.assertRegex(rr, self.pattern.railroad())

        for i_rr in invalid_rr:
            self.assertNotRegex(i_rr, self.pattern.railroad())

    def test_extract_player_name(self):
        data = dict(Petesuchos='Petesuchos chooses a company', Burgos='Burgos chooses a company',
                    Rivaben='Rivaben chooses a company', ftola='ftola chooses a company',
                    jjrbedford='jjrbedford chooses a company', discoking7='discoking7 chooses a company',
                    Korval='Korval chooses a company')

        compiled_regex = re.compile(self.pattern.introduce_player())
        for player, text in data.items():
            result = compiled_regex.match(text)
            self.assertEqual(player, result.group('player'))

    def test_stock_round(self):
        data = {
            1: '-- Stock Round 1 --',
            2: '-- Stock Round 2 --',
            9: '-- Stock Round 9 --',
            10: '-- Stock Round 10 --',
            19: '-- Stock Round 19 --',
            123: '-- Stock Round 123 --'
        }

        compiled_regex = re.compile(self.pattern.stock_round())
        for sr, text in data.items():
            result = compiled_regex.match(text)
            self.assertEqual(sr, int(result.group('stock_round')))

        self.assertIsNone(compiled_regex.match('-- Stock Round XYZ --'))
