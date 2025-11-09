class Player:
    def __init__(self, data):
        self.name = data['name']
        self.team = data['team']
        self.goals = data['goals']
        self.assists = data['assists']
        self.nationality = data['nationality']

    @property
    def points(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} {self.team:14} {self.goals} + {self.assists} = {self.points}"
