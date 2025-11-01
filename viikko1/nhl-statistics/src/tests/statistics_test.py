import unittest
from statistics_service import StatisticsService, SortBy
from player import Player


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]


class TestStatisticsService(unittest.TestCase):
    def test_palauttaa_pelaajat(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.assertEqual(str(self.stats.search('Gretzky')), 'Gretzky EDM 35 + 89 = 124')

    def test_palauttaa_none_jos_nimea_ei_loydy(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.assertEqual(str(self.stats.search('asdf123')), 'None')

    def test_palauttaa_EDM_pelaajat(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.assertEqual(str(list(self.stats.team('EDM'))[0]), 'Semenko EDM 4 + 12 = 16')
        self.assertEqual(str(list(self.stats.team('EDM'))[1]), 'Kurri EDM 37 + 53 = 90')
        self.assertEqual(str(list(self.stats.team('EDM'))[2]), 'Gretzky EDM 35 + 89 = 124')

    def test_palauttaa_top_points(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.assertEqual(str(list(self.stats.top(1, SortBy.POINTS))[0]), 'Gretzky EDM 35 + 89 = 124')

    def test_palauttaa_top_goals(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.assertEqual(str(list(self.stats.top(1, SortBy.GOALS))[0]), 'Lemieux PIT 45 + 54 = 99')

    def test_palauttaa_top_assists(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.assertEqual(str(list(self.stats.top(1, SortBy.ASSISTS))[0]), 'Gretzky EDM 35 + 89 = 124')