from vrbr18xx.corporation import Corporations
from vrbr18xx.player import Player


class GameState(object):

    def __init__(self, game: str = '1846', initial_cash_for_players: int = 400):
        self.players = {}
        self.initial_cash = initial_cash_for_players
        self.game = game
        self.corporations = Corporations()
        self.game_round = 'Start'

    def add_player(self, player_name: str):
        player = Player(player_name, self.initial_cash)
        if player not in self.players:
            self.players[player.name] = player

    def buy_shares(self, player_name: str, company_name: str, price: int, quantity: int = 1):
        self.players[player_name].buy_shares(company_name, price, quantity)
    
    def sell_shares(self, player_name: str, company_name: str, price: int, quantity: int = 1):
        self.players[player_name].sell_shares(company_name, price, quantity)

    def par_company(self, company_name: str, price: int):
        self.corporations.par(company_name, price)

    def set_company_price(self, company_name: str, new_price: int):
        self.corporations.set_price(company_name, new_price)

    def evaluate_player(self, player_name: str) -> int:
        if player_name not in self.players.keys():
            raise ValueError('Player not found.')

        player = self.players[player_name]
        assets_value = player.cash
        for company_name, shares in player.shares.items():
            assets_value += self.corporations[company_name] * shares
        return assets_value

    def player_receives(self, player_name: str, money:int):
        self.players[player_name].cash += money

    def store_valuation(self):
        for player in self.players.values():
            player.store_valuation(self.game_round, self.evaluate_player(player.name))

    def set_stock_round(self, sr: str):
        self.game_round = 'SR '+sr

    def set_operation_round(self, opr: str):
        self.game_round = 'OR '+opr

