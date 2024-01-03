from lambda_function import lambda_handler
from DogfightSimulator import DogfightSimulator
from Animations import Animations
import unittest

class Test_lambda_function(unittest.TestCase):
    def test_sampleBattle(self):
        simulator = DogfightSimulator("10,10,8,8,9,9,20,15,7,7", "34,31,36,30,28,25,2,2", Animations())
        simulator.simulateDogfight()
        print("new fight")
        print(simulator.startingDeckOne)
        print(simulator.startingDeckTwo)
        print('*'.join(simulator.animations.animationsList))
        assert simulator.playerOne != None
        assert simulator.playerTwo != None

    """def test_monteCarlosSimulator(self):
        oneWins = 0
        onePoints = 0
        twoWins = 0
        twoPoints = 0
        ties = 0
        timesToRunSimulation = 1000
        for x in range(0,timesToRunSimulation):
            simulator = DogfightSimulator("38,38,39,39,40,40,41,41,42,42", "8,9,8,9,18,18,20,20,10,10", Animations())
            simulator.simulateDogfight()
            lastAnimationCode = simulator.animations.animationsList.pop()
            if ("1w" in lastAnimationCode):
                oneWins += 1
                onePoints += simulator.playerOne.pointsScored()
            elif ("2w" in lastAnimationCode):
                twoWins += 1
                twoPoints += simulator.playerTwo.pointsScored()
            elif ("ft" in lastAnimationCode):
                ties += 1
        print("team one: " + str(oneWins))
        print("team two: " + str(twoWins))
        print("teams tie: " + str(ties))
        print("team one points: " + str(onePoints))
        print("team two points: " + str(twoPoints))
        assert (oneWins + twoWins + ties) == timesToRunSimulation"""