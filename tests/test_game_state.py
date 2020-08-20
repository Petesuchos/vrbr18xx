from unittest import TestCase
from vrbr18xx.gamestate import GameState
from vrbr18xx.player import Player


class TestGame(TestCase):

    def test_init(self):
        game = GameState()
        self.assertTrue(len(game.players) == 0)

    def test_add_player(self):
        game = GameState()
        game.add_player(player_name='Cake')
        self.assertTrue(len(game.players) == 1)
        self.assertEqual(game.players['Cake'], Player(name='Cake', initial_cash=100))
        game.add_player(player_name='Meow')
        self.assertTrue(len(game.players) == 2)

    def test_add_repeated_player(self):
        game = GameState()
        game.add_player(player_name='Cake')
        game.add_player(player_name='Cake')
        self.assertTrue(len(game.players) == 1)

    def test_evaluate_player_not_found(self):
        game = GameState()
        with self.assertRaises(ValueError):
            game.evaluate_player(player_name='Canelinha')

    def test_evaluate_player(self):
        game = GameState(initial_cash_for_players=400)
        game.add_player(player_name='Cake')
        self.assertEqual(400, game.evaluate_player('Cake'))
        game.par_company(company_name='NYC', price=50)
        game.buy_shares(player_name='Cake', company_name='NYC', price=50, quantity=2)
        self.assertEqual(400, game.evaluate_player('Cake'))
        game.set_company_price(company_name='NYC', new_price=100)
        self.assertEqual(500, game.evaluate_player('Cake'))
        game.sell_shares(player_name='Cake', company_name='NYC', price=200, quantity=1)
        self.assertEqual(600, game.evaluate_player('Cake'))

    def test_evaluate_player_multiple_shares(self):
        game = GameState(initial_cash_for_players=200)
        game.add_player(player_name='Dwight')
        self.assertEqual(200, game.evaluate_player('Dwight'))
        game.par_company(company_name='PRR', price=50)
        game.par_company(company_name='B&O', price=100)
        game.buy_shares(player_name='Dwight', company_name='PRR', price=50, quantity=2)
        game.buy_shares(player_name='Dwight', company_name='B&O', price=100, quantity=1)
        self.assertEqual(200, game.evaluate_player('Dwight'))

    def test_evaluate_player_share_fluctuation(self):
        game = GameState(initial_cash_for_players=500)
        game.add_player(player_name='Barbara')
        game.par_company(company_name='IC', price=50)
        game.buy_shares(player_name='Barbara', company_name='IC', price=50, quantity=1)
        self.assertEqual(500, game.evaluate_player('Barbara'))
        game.set_company_price(company_name='IC', new_price=0)
        self.assertEqual(450, game.evaluate_player('Barbara'))

    def test_store_valuation(self):
        game = GameState(initial_cash_for_players=100)
        game.add_player(player_name='John')
        game.add_player(player_name='Paul')
        game.store_valuation()
        self.assertEqual(100, game.players['John'].valuation['Start'])
        self.assertEqual(100, game.players['Paul'].valuation['Start'])

        game.game_round = 'OR1.1'
        game.par_company(company_name='NYC', price=50)
        game.buy_shares(player_name='John', company_name='NYC', price=50, quantity=2)
        game.set_company_price(company_name='NYC', new_price=500)
        game.players['Paul'].cash = 10
        game.store_valuation()
        self.assertEqual(1000, game.players['John'].valuation['OR1.1'])
        self.assertEqual(10, game.players['Paul'].valuation['OR1.1'])

    def test_player_receives(self):
        game = GameState(initial_cash_for_players=600)
        game.add_player(player_name='Nellie')
        game.players['Nellie'].cash += 50
        self.assertEqual(650, game.players['Nellie'].cash)

    def test_set_stock_round(self):
        game = GameState()
        self.assertEqual('Start', game.game_round)
        game.set_stock_round('1')
        self.assertEqual('SR 1', game.game_round)
        game.set_stock_round('2')
        self.assertEqual('SR 2', game.game_round)
        game.set_stock_round('99')
        self.assertEqual('SR 99', game.game_round)

    def test_set_operation_round(self):
        game = GameState()
        self.assertEqual('Start', game.game_round)
        game.set_operation_round('1.1')
        self.assertEqual('OR 1.1', game.game_round)
        game.set_operation_round('1.2')
        self.assertEqual('OR 1.2', game.game_round)
        game.set_operation_round('5.2')
        self.assertEqual('OR 5.2', game.game_round)
