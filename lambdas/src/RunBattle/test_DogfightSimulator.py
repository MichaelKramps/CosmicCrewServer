from DogfightSimulator import DogfightSimulator
from Animations import Animations
from Cards import Card
import unittest

class Test_DogfightSimulator(unittest.TestCase):
    def setUp(self):
        Animations.clearAnimations()

    def test_setsPlayers(self):
        simulator = DogfightSimulator("1", "1")
        assert simulator.playerOne != None
        assert simulator.playerTwo != None

    def test_simulateDogfightSetsStartingDecks(self):
        simulator = DogfightSimulator("1", "1")
        simulator.simulateDogfight()
        assert simulator.startingDeckOne != None
        assert simulator.startingDeckTwo != None

    def test_getStartingDeckStringIsCorrect(self):
        simulator = DogfightSimulator("1", "1")
        testDeck = [Card("test", 23, 0, []), Card("test", 16, 0, []), Card("test", 127, 0, []), Card("test", 1, 0, []), Card("test", 6, 0, [])]
        assert simulator.getStartingDeckString(testDeck) == "23,16,127,1,6"

    def test_setupDogfightOneAndTwoCards(self):
        simulator = DogfightSimulator("1", "1,1")
        simulator.setupDogfight()
        assert simulator.playerOne.team[0] != None
        assert simulator.playerOne.team[1] == None
        assert simulator.playerOne.team[2] == None
        assert simulator.playerOne.team[3] == None
        assert simulator.playerOne.team[4] == None
        assert simulator.playerOne.team[5] == None
        assert simulator.playerTwo.team[0] != None
        assert simulator.playerTwo.team[1] != None
        assert simulator.playerTwo.team[2] == None
        assert simulator.playerTwo.team[3] == None
        assert simulator.playerTwo.team[4] == None
        assert simulator.playerTwo.team[5] == None

    def test_setupDogfightThreeAndFourCards(self):
        simulator = DogfightSimulator("1,1,1", "1,1,1,1")
        simulator.setupDogfight()
        assert simulator.playerOne.team[0] != None
        assert simulator.playerOne.team[1] != None
        assert simulator.playerOne.team[2] != None
        assert simulator.playerOne.team[3] == None
        assert simulator.playerOne.team[4] == None
        assert simulator.playerOne.team[5] == None
        assert simulator.playerTwo.team[0] != None
        assert simulator.playerTwo.team[1] != None
        assert simulator.playerTwo.team[2] != None
        assert simulator.playerTwo.team[3] != None
        assert simulator.playerTwo.team[4] == None
        assert simulator.playerTwo.team[5] == None

    def test_setupDogfightFiveAndSixCards(self):
        simulator = DogfightSimulator("1,1,1,1,1", "1,1,1,1,1,1")
        simulator.setupDogfight()
        assert simulator.playerOne.team[0] != None
        assert simulator.playerOne.team[1] != None
        assert simulator.playerOne.team[2] != None
        assert simulator.playerOne.team[3] != None
        assert simulator.playerOne.team[4] != None
        assert simulator.playerOne.team[5] == None
        assert simulator.playerTwo.team[0] != None
        assert simulator.playerTwo.team[1] != None
        assert simulator.playerTwo.team[2] != None
        assert simulator.playerTwo.team[3] != None
        assert simulator.playerTwo.team[4] != None
        assert simulator.playerTwo.team[5] != None

    def test_setupDogfightSevenAndMoreCards(self):
        simulator = DogfightSimulator("1,1,1,1,1,1,1", "1,1,1,1,1,1,1,1,1,1,1,1")
        simulator.setupDogfight()
        assert simulator.playerOne.team[0] != None
        assert simulator.playerOne.team[1] != None
        assert simulator.playerOne.team[2] != None
        assert simulator.playerOne.team[3] != None
        assert simulator.playerOne.team[4] != None
        assert simulator.playerOne.team[5] != None
        assert simulator.playerTwo.team[0] != None
        assert simulator.playerTwo.team[1] != None
        assert simulator.playerTwo.team[2] != None
        assert simulator.playerTwo.team[3] != None
        assert simulator.playerTwo.team[4] != None
        assert simulator.playerTwo.team[5] != None

    def test_fightHasCorrectWinnerInGuaranteedPlayerOneWin(self):
        simulator = DogfightSimulator("1,1,1,1,1,1,1", "0,0,0,0,0,0,0,0")
        simulator.simulateDogfight()#fight called inside here
        assert "p,1w,0,0" in Animations.animationsList

    def test_fightHasCorrectWinnerInGuaranteedPlayerTwoWin(self):
        simulator = DogfightSimulator("0,0,0,0,0,0,0,0", "1,1,1,1,1,1,1")
        simulator.simulateDogfight()#fight called inside here
        assert "s,2w,0,0" in Animations.animationsList

    def test_fightTiesInGuaranteedTie(self):
        simulator = DogfightSimulator("0,0,0,0,0,0,0,0", "0,0,0,0,0,0,0,0")
        simulator.simulateDogfight()#fight called inside here
        assert "b,ft,0,0" in Animations.animationsList