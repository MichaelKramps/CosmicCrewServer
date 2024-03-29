from lambda_function import lambda_handler
from DogfightSimulator import DogfightSimulator
from Animations import Animations
import unittest
import random

class Test_lambda_function(unittest.TestCase):
    def test_sampleBattle(self):
        simulator = DogfightSimulator(self.randomDeckString(), self.randomDeckString(), Animations())
        simulator.simulateDogfight()
        print("new fight")
        print(simulator.startingDeckOne)
        print(simulator.startingDeckTwo)
        print('*'.join(simulator.animations.animationsList))
        assert simulator.playerOne != None
        assert simulator.playerTwo != None

    def test_monteCarlosSimulator(self):
        oneWins = 0
        onePoints = 0
        twoWins = 0
        twoPoints = 0
        ties = 0
        timesToRunSimulation = 1000
        for x in range(0,timesToRunSimulation):
            simulator = DogfightSimulator(self.randomDeckString(), self.randomDeckString(), Animations())
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
        assert (oneWins + twoWins + ties) == timesToRunSimulation

    def randomDeckString(self):
        deckString = ""
        for card in range(0,12):
            if card != 0:
                deckString += ","
            thisCardId = random.randint(0,70)
            deckString += str(thisCardId)
        return deckString