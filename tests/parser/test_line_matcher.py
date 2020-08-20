from unittest import TestCase
from vrbr18xx.parser.parser import Match, LineMatcher, LineMatcherFabric


class TestLineMatcher(TestCase):
    def test_add_player(self):
        fabric = LineMatcherFabric()
        add_player_matcher = fabric.add_player_matcher()

        line = 'Petesuchos chooses a company'
        match = add_player_matcher.match(line)
        self.assertEqual('add_player', match.action)
        self.assertEqual('Petesuchos', match.results['player'])

        line = 'ftola chooses a company'
        match = add_player_matcher.match(line)
        self.assertEqual('add_player', match.action)
        self.assertEqual('ftola', match.results['player'])

        line = 'Neque porro quisquam est qui dolorem'
        match = add_player_matcher.match(line)
        self.assertIsNone(match)

    def test_stock_round(self):
        fabric = LineMatcherFabric()
        stock_round_matcher = fabric.stock_round_matcher()

        line = '-- Stock Round 1 --'
        match = stock_round_matcher.match(line)
        self.assertEqual('stock_round', match.action)
        self.assertEqual('1', match.results['stock_round'])

        line = '-- Stock Round 5 --'
        match = stock_round_matcher.match(line)
        self.assertEqual('stock_round', match.action)
        self.assertEqual('5', match.results['stock_round'])

        line = 'Neque porro quisquam est qui dolorem'
        match = stock_round_matcher.match(line)
        self.assertIsNone(match)

    def test_operating_round(self):
        fabric = LineMatcherFabric()
        operating_round_matcher = fabric.operation_round_matcher()

        line = '-- Operating Round 1.2 (of 2) --'
        match = operating_round_matcher.match(line)
        self.assertEqual('operation_round', match.action)
        self.assertEqual('1.2', match.results['operation_round'])

        line = '-- Operating Round 3.1 (of 2) --'
        match = operating_round_matcher.match(line)
        self.assertEqual('operation_round', match.action)
        self.assertEqual('3.1', match.results['operation_round'])

        line = 'Neque porro quisquam est qui dolorem'
        match = operating_round_matcher.match(line)
        self.assertIsNone(match)

    def test_par(self):
        fabric = LineMatcherFabric()
        par_matcher = fabric.par_matcher()

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

        line = 'Neque porro quisquam est qui dolorem'
        match = par_matcher.match(line)
        self.assertIsNone(match)

    def test_buy_shares(self):
        fabric = LineMatcherFabric()
        buy_matcher = fabric.buy_shares_matcher()

        line = 'Petesuchos buys a 20% share of NYC from the Treasury for $300'
        match = buy_matcher.match(line)
        self.assertEqual('buy_shares', match.action)
        self.assertEqual('Petesuchos', match.results['player'])
        self.assertEqual('NYC', match.results['corporation'])
        self.assertEqual('300', match.results['value'])

        line = 'Neque porro quisquam est qui dolorem'
        match = buy_matcher.match(line)
        self.assertIsNone(match)

    def test_sell_shares(self):
        fabric = LineMatcherFabric()
        sell_matcher = fabric.sell_shares_matcher()

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

        line = 'Neque porro quisquam est qui dolorem'
        match = sell_matcher.match(line)
        self.assertIsNone(match)

    def test_corporation_price_change(self):
        fabric = LineMatcherFabric()
        price_change_matcher = fabric.corporation_price_change_matcher()

        line = 'GT\'s share price changes from $137 to $124'
        match = price_change_matcher.match(line)
        self.assertEqual('corporation_share_price_change', match.action)
        self.assertEqual('GT', match.results['corporation'])
        self.assertEqual('124', match.results['value'])

        line = 'Neque porro quisquam est qui dolorem'
        match = price_change_matcher.match(line)
        self.assertIsNone(match)

    def test_player_receives(self):
        fabric = LineMatcherFabric()
        player_receives_matcher = fabric.player_receives_matcher()

        line = 'Burgos receives $190 = $38 x 5 shares'
        match = player_receives_matcher.match(line)
        self.assertEqual('player_receives', match.action)
        self.assertEqual('Burgos', match.results['player'])
        self.assertEqual('190', match.results['value'])

        line = 'IC receives $152 = $38 x 4 shares'
        match = player_receives_matcher.match(line)
        self.assertIsNone(match)

        line = 'Neque porro quisquam est qui dolorem'
        match = player_receives_matcher.match(line)
        self.assertIsNone(match)