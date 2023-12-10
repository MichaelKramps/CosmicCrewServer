from lambda_function import lambda_handler
from DogfightSimulator import DogfightSimulator
from Animations import Animations
import unittest

class Test_lambda_function(unittest.TestCase):
    def test_sampleBattle(self):
        simulator = DogfightSimulator("20,21,22,23,24,25,26,27,28,29,30,31", "20,21,22,23,24,25,26,27,28,29,30,31", Animations())
        simulator.simulateDogfight()
        print(simulator.startingDeckOne)
        print(simulator.startingDeckTwo)
        print('*'.join(simulator.animations.animationsList))
        assert simulator.playerOne != None
        assert simulator.playerTwo != None