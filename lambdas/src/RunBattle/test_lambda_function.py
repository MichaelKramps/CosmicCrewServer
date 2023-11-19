from lambda_function import lambda_handler
from DogfightSimulator import DogfightSimulator
from Animations import Animations
import unittest

class Test_lambda_function(unittest.TestCase):
    def test_setsPlayers(self):
        simulator = DogfightSimulator("1", "1", Animations())
        assert simulator.playerOne != None
        assert simulator.playerTwo != None