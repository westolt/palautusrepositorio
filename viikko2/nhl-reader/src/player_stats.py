class PlayerStats:
    def __init__(self, reader):
        self.all_players = reader.get_players()

    def top_scorers_by_nationality(self, nationality_input):
        result = []

        for player in self.all_players:
            if player.nationality == nationality_input:
                result.append(player)
        
        result = sorted(result, key=lambda player : player.points, reverse=True)

        return result