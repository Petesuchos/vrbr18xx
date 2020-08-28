from unittest import TestCase
from vrbr18xx.controller import Controller


class TestController(TestCase):

    def test_controller(self):
        with open('./data/1846/game04') as data_file:
            data = data_file.readlines()
        controller = Controller(data)
        controller.run()
        for player_name, player in controller.state.players.items():
            print(player_name, player.valuation)