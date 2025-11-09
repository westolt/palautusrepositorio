from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats

def show_players_table(players, season, nationality):
    table = Table(title=f"Season {season} players from {nationality}")
    table.add_column('Name', style='blue')
    table.add_column('Team', style='red')
    table.add_column('Goals', justify='right', style='green')
    table.add_column('Assists', justify='right', style='green')
    table.add_column('Points', justify='right', style='yellow')

    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points)
        )

    return table

def nationality_loop(console, stats, season):
    nationality = console.input('Choose nationality [FIN, SWE, CAN, USA...]: ')
    while nationality != '0':
        players = stats.top_scorers_by_nationality(nationality)
        table = show_players_table(players, season, nationality)
        console.print(table)

        console.print('Type 0 to quit', style='red')
        nationality = console.input('Choose nationality: ')

def main():
    console = Console()
    season = console.input('Choose season: [2018-19 / 2019-20 .../ 2024-25]: ')
    url = f'https://studies.cs.helsinki.fi/nhlstats/{season}/players'
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationality_loop(console, stats, season)

if __name__ == "__main__":
    main()
