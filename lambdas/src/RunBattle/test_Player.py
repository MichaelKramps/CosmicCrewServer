from Player import Player
import unittest

class Test_Player(unittest.TestCase):

    def setsPlayerIdentifier(self):
        player = Player("1", "p")
        assert player.playerIdentifier == "p"