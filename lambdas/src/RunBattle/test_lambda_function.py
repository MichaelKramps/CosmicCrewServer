from lambda_function import lambda_handler
from DogfightSimulator import DogfightSimulator
from Animations import Animations
import unittest

class Test_lambda_function(unittest.TestCase):
    def test_sampleBattle(self):
        simulator = DogfightSimulator("3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20", "21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37", Animations())
        simulator.simulateDogfight()
        print(simulator.startingDeckOne)
        print(simulator.startingDeckTwo)
        print('*'.join(simulator.animations.animationsList))
        assert simulator.playerOne != None
        assert simulator.playerTwo != None

    def test_monteCarlosSimulator(self):
        oneWins = 0
        twoWins = 0
        ties = 0
        timesToRunSimulation = 1000
        for x in range(0,timesToRunSimulation):
            simulator = DogfightSimulator("3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20", "21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37", Animations())
            simulator.simulateDogfight()
            lastAnimationCode = simulator.animations.animationsList.pop()
            if ("1w" in lastAnimationCode):
                oneWins += 1
            elif ("2w" in lastAnimationCode):
                twoWins += 1
            elif ("ft" in lastAnimationCode):
                ties += 1
        print("team one: " + str(oneWins))
        print("team two: " + str(twoWins))
        print("teams tie: " + str(ties))
        assert (oneWins + twoWins + ties) == timesToRunSimulation