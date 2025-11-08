import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = []

    nationality_input = input('Give nationality: ')

    for player_dict in response:
        player = Player(player_dict)
        if player.nationality == nationality_input:
            players.append(player)

    print(f"Players from {nationality_input}:")

    for player in players:
        print(player)

if __name__ == "__main__":
    main()
