from vrbr18xx.gamestate import GameState
from vrbr18xx.parser import *


class Controller:

    def __init__(self, data: str = None):
        self.state = GameState()
        self.matchers = SentenceMatcherFabric(self).get_all()
        self.data = data

    def notify(self, match: Match):
        if match.action == 'add_player':
            self.state.add_player(match.results['player'])
        if match.action == 'stock_round':
            self.state.set_stock_round(match.results['stock_round'])
            self.state.store_valuation()
        if match.action == 'operation_round':
            self.state.set_operation_round(match.results['operation_round'])
            self.state.store_valuation()
        if match.action == 'par':
            self.state.par_company(match.results['corporation'], int(match.results['value']))
        if match.action == 'buy_shares':
            self.state.buy_shares(
                match.results['player'],
                match.results['corporation'],
                int(match.results['value']),
                int(match.results['shares']) / 10
            )
        if match.action == 'sell_shares':
            self.state.sell_shares(
                match.results['player'],
                match.results['corporation'],
                int(match.results['value']),
                int(match.results['number_of_shares'])
            )
        if match.action == 'corporation_share_price_change':
            self.state.set_company_price(
                match.results['corporation'],
                int(match.results['value'])
            )
        if match.action == 'player_receives':
            self.state.player_receives(
                match.results['player'],
                int(match.results['value'])
            )
        if match.action == 'player_buys_private':
            self.state.player_receives(
                match.results['player'],
                int(match.results['value']) * -1
            )
        if match.action == 'player_collects':
            self.state.player_receives(
                match.results['player'],
                int(match.results['value'])
            )

    def run(self):
        if self.data is None:
            raise ValueError('No data to calculate')

        for sentence in self.data:
            for matcher in self.matchers:
                matcher.match(sentence)
        self.state.store_valuation()
