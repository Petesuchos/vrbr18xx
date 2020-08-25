from unittest import TestCase
from vrbr18xx.parser.parser import Match, SentenceMatcher, SentenceMatcherFabric


class TestLineMatcher(TestCase):
    def test_add_player(self):
        fabric = SentenceMatcherFabric()
        add_player_matcher = fabric.get_add_player_matcher()

        line = 'Petesuchos chooses a company'
        match = add_player_matcher.match(line)
        self.assertEqual('add_player', match.action)
        self.assertEqual('Petesuchos', match.results['player'])

        line = 'ftola chooses a company'
        match = add_player_matcher.match(line)
        self.assertEqual('add_player', match.action)
        self.assertEqual('ftola', match.results['player'])

    def test_stock_round(self):
        fabric = SentenceMatcherFabric()
        stock_round_matcher = fabric.get_stock_round_matcher()

        line = '-- Stock Round 1 --'
        match = stock_round_matcher.match(line)
        self.assertEqual('stock_round', match.action)
        self.assertEqual('1', match.results['stock_round'])

        line = '-- Stock Round 5 --'
        match = stock_round_matcher.match(line)
        self.assertEqual('stock_round', match.action)
        self.assertEqual('5', match.results['stock_round'])

    def test_operating_round(self):
        fabric = SentenceMatcherFabric()
        operating_round_matcher = fabric.get_operation_round_matcher()

        line = '-- Operating Round 1.2 (of 2) --'
        match = operating_round_matcher.match(line)
        self.assertEqual('operation_round', match.action)
        self.assertEqual('1.2', match.results['operation_round'])

        line = '-- Operating Round 3.1 (of 2) --'
        match = operating_round_matcher.match(line)
        self.assertEqual('operation_round', match.action)
        self.assertEqual('3.1', match.results['operation_round'])

    def test_par(self):
        fabric = SentenceMatcherFabric()
        par_matcher = fabric.get_par_matcher()

        line = 'Burgos pars IC at $100'
        match = par_matcher.match(line)
        self.assertEqual('par', match.action)
        self.assertEqual('Burgos', match.results['player'])
        self.assertEqual('IC', match.results['corporation'])
        self.assertEqual('100', match.results['value'])

        line = 'Rivaben pars ERIE at $60'
        match = par_matcher.match(line)
        self.assertEqual('par', match.action)
        self.assertEqual('Rivaben', match.results['player'])
        self.assertEqual('ERIE', match.results['corporation'])
        self.assertEqual('60', match.results['value'])

    def test_buy_shares(self):
        fabric = SentenceMatcherFabric()
        buy_matcher = fabric.get_buy_shares_matcher()

        line = 'Petesuchos buys a 20% share of NYC from the Treasury for $300'
        match = buy_matcher.match(line)
        self.assertEqual('buy_shares', match.action)
        self.assertEqual('Petesuchos', match.results['player'])
        self.assertEqual('NYC', match.results['corporation'])
        self.assertEqual('300', match.results['value'])

    def test_sell_shares(self):
        fabric = SentenceMatcherFabric()
        sell_matcher = fabric.get_sell_shares_matcher()

        line = 'Petesuchos sells 1 share NYC and receives $112'
        match = sell_matcher.match(line)
        self.assertEqual('sell_shares', match.action)
        self.assertEqual('Petesuchos', match.results['player'])
        self.assertEqual('1', match.results['number_of_shares'])
        self.assertEqual('NYC', match.results['corporation'])
        self.assertEqual('112', match.results['value'])

        line = 'Burgos sells 2 shares B&O and receives $224'
        match = sell_matcher.match(line)
        self.assertEqual('sell_shares', match.action)
        self.assertEqual('Burgos', match.results['player'])
        self.assertEqual('2', match.results['number_of_shares'])
        self.assertEqual('B&O', match.results['corporation'])
        self.assertEqual('224', match.results['value'])

    def test_corporation_price_change(self):
        fabric = SentenceMatcherFabric()
        price_change_matcher = fabric.get_corporation_price_change_matcher()

        line = 'GT\'s share price changes from $137 to $124'
        match = price_change_matcher.match(line)
        self.assertEqual('corporation_share_price_change', match.action)
        self.assertEqual('GT', match.results['corporation'])
        self.assertEqual('124', match.results['value'])

    def test_player_receives(self):
        fabric = SentenceMatcherFabric()
        player_receives_matcher = fabric.get_player_receives_matcher()

        line = 'Burgos receives $190 = $38 x 5 shares'
        match = player_receives_matcher.match(line)
        self.assertEqual('player_receives', match.action)
        self.assertEqual('Burgos', match.results['player'])
        self.assertEqual('190', match.results['value'])

        line = 'IC receives $152 = $38 x 4 shares'
        match = player_receives_matcher.match(line)
        self.assertIsNone(match)

    def test_chat(self):
        fabric = SentenceMatcherFabric()
        chat_matcher = fabric.get_chat_matcher()

        line = 'Rivaben: tow no pass tb'
        match = chat_matcher.match(line)
        self.assertIsNotNone(match)

    def test_player_buys_private(self):
        fabric = SentenceMatcherFabric()
        player_buys_private_matcher = fabric.get_player_buys_private_matcher()
        line = 'Petesuchos buys Ohio & Indiana for $40'
        match = player_buys_private_matcher.match(line)
        self.assertEqual('player_buys_private', match.action)
        self.assertEqual('Petesuchos', match.results['player'])
        self.assertEqual('Ohio & Indiana', match.results['private'])
        self.assertEqual('40', match.results['value'])

    def test_player_collects(self):
        fabric = SentenceMatcherFabric()
        player_collects = fabric.get_player_collects_matcher()
        line = 'Rivaben collects $15 from Lake Shore Line'
        match = player_collects.match(line)
        self.assertEqual('player_collects', match.action)
        self.assertEqual('Rivaben', match.results['player'])
        self.assertEqual('15', match.results['value'])
        self.assertEqual('Lake Shore Line', match.results['private'])
