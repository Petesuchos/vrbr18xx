from unittest import TestCase
from vrbr18xx.parser import *


class TestMultipleSentences(TestCase):
    def test_get_all_sentence_matchers(self):
        class MockInterpreterCoordinator:
            def notify(self, match: Match):
                print(match)
                return match

        sentence_matchers = SentenceMatcherFabric(MockInterpreterCoordinator()).get_all()

        sentences = {  # key: expected action, value: sentence
            'add_player': 'Rivaben chooses a company',
            'stock_round': '-- Stock Round 1 --',
            'operation_round': '-- Operating Round 1.1 (of 2) --',
            'par': 'Petesuchos pars C&O at $137',
            'buy_shares': 'Petesuchos buys a 20% share of C&O from the Treasury for $274',
            'sell_shares': 'Burgos sells 2 shares B&O and receives $224',
            'corporation_share_price_change': "IC's share price changes from $112 to $137",
            'player_receives': 'Rivaben receives $195 = $39 x 5 shares',
            'player_buys_private': 'ftola buys Big 4 for $100',
            'player_collects': 'Burgos collects $10 from Chicago and Western Indiana',
            'chat': 'ftola: tou no pass!'
        }

        for expected_action, sentence in sentences.items():
            for matcher in sentence_matchers:
                match = matcher.match(sentence)
                if match is not None:
                    self.assertEqual(expected_action, match.action)
