import requests
from player import Player

class PlayerReader: # pylint: disable=too-few-public-methods
    def __init__(self, url):
        self.url = url

    def get_players(self):
        try:
            response = requests.get(self.url, timeout=1).json()
        except requests.Timeout as err:
            print(err)

        players = []

        for player_dict in response:
            player = Player(player_dict)
            players.append(player)

        return players
