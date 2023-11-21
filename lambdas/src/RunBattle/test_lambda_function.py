from lambda_function import lambda_handler
from DogfightSimulator import DogfightSimulator
from Animations import Animations
import unittest

class Test_lambda_function(unittest.TestCase):
    def test_setsPlayers(self):
        simulator = DogfightSimulator("7,11,0,12,12,13,8,9,8", "0,1,2,3,4,5,6,7,8,9,10,11,12,13", Animations())
        simulator.simulateDogfight()
        print(simulator.startingDeckOne)
        print(simulator.startingDeckTwo)
        print('*'.join(simulator.animations.animationsList))
        assert simulator.playerOne != None
        assert simulator.playerTwo != None