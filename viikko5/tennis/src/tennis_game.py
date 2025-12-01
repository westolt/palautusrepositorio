class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def get_even_score(self):
        if self.m_score1 == 0:
            return "Love-All"
        elif self.m_score1 == 1:
            return "Fifteen-All"
        elif self.m_score1 == 2:
            return "Thirty-All"
        else:
            return "Deuce"
        
    def get_advantage_score(self, score1, score2):
        difference = score1 - score2

        if difference == 1:
            return "Advantage player1"
        if difference == -1:
            return "Advantage player2"
        if difference >= 2:
            return "Win for player1"

        return "Win for player2"
        
    def give_score_to_player(self, score1, score2):
        score = ""
        current_score = 0

        for i in range(1, 3):

            if i == 1:
                current_score = score1
            else:
                score = score + "-"
                current_score = score2

            if current_score == 0:
                score = score + "Love"
            elif current_score == 1:
                score = score + "Fifteen"
            elif current_score == 2:
                score = score + "Thirty"
            elif current_score == 3:
                score = score + "Forty"

        return score

    def get_score(self):

        if self.m_score1 == self.m_score2:
            return self.get_even_score()

        if self.m_score1 >= 4 or self.m_score2 >= 4:
            return self.get_advantage_score(self.m_score1, self.m_score2)
        return self.give_score_to_player(self.m_score1, self.m_score2)
