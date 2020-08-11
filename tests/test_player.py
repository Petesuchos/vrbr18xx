from unittest import TestCase
from vrbr18xx.player import Player


class TestPlayer(TestCase):

    def test_init(self):
        player1 = Player(name='Petesuchos', initial_cash=400)
        self.assertEqual(player1.name, 'Petesuchos')
        self.assertEqual(player1.cash, 400)
        self.assertDictEqual(player1.shares, {})

    def test_eq(self):
        player1 = Player(name='Petesuchos', initial_cash=400)
        player2 = Player(name='Petesuchos', initial_cash=800)
        player3 = Player(name='Flambo', initial_cash=0)

        self.assertEqual(player1, player1)
        self.assertEqual(player1, player2)
        self.assertNotEqual(player1, player3)

    def test_buy_shares(self):
        player = Player('Joe', 400)
        player.buy_shares(company_name='PRR', price=50, quantity=2)
        self.assertEqual(player.cash, 300)
        self.assertEqual(player.PRR, 2)

        player.buy_shares(company_name='PRR', price=100, quantity=1)
        self.assertEqual(player.cash, 200)
        self.assertEqual(player.PRR, 3)

    def test_sell_shares(self):
        player = Player('Mike', 200)
        player.buy_shares(company_name='NYC', price=50, quantity=4)
        self.assertEqual(player.cash, 0)
        self.assertEqual(player.NYC, 4)

        player.sell_shares(company_name='NYC', price=100, quantity=3)
        self.assertEqual(player.cash, 300)
        self.assertEqual(player.NYC, 1)

    def test_sell_more_shares_than_owned(self):
        player = Player('Fry', 200)
        player.buy_shares(company_name='GT', price=50, quantity=1)

        with self.assertRaises(ValueError):
            player.sell_shares(company_name='GT', price=100, quantity=2)

    def test_sell_shares_not_owned_company(self):
        player = Player('Guadalupe', 200)
        player.buy_shares(company_name='NYC', price=50, quantity=1)

        with self.assertRaises(ValueError):
            player.sell_shares(company_name='PRR', price=100, quantity=1)

    def test_store_valuation(self):
        player = Player('Selma', 100)
        player.store_valuation(round_phase='SR1', valuation=100)
        player.store_valuation(round_phase='OR1.1', valuation=80)
        player.store_valuation(round_phase='OR1.2', valuation=120)
        self.assertEqual(3, len(player.valuation))


