from DogfightSimulator import DogfightSimulator
from Animations import Animations
from Cards import Card
import unittest

class Test_DogfightSimulator(unittest.TestCase):
    def test_setsPlayers(self):
        simulator = DogfightSimulator("1", "1", Animations())
        assert simulator.playerOne != None
        assert simulator.playerTwo != None

    def test_simulateDogfightSetsStartingDecks(self):
        simulator = DogfightSimulator("1", "1", Animations())
        simulator.simulateDogfight()
        assert simulator.startingDeckOne != None
        assert simulator.startingDeckTwo != None

    def test_getStartingDeckStringIsCorrect(self):
        animations = Animations()
        simulator = DogfightSimulator("1", "1", animations)
        testDeck = [Card("test", 23, 0, [], animations), Card("test", 16, 0, [], animations), Card("test", 127, 0, [], animations), Card("test", 1, 0, [], animations), Card("test", 6, 0, [], animations)]
        assert simulator.getStartingDeckString(testDeck) == "23,16,127,1,6"

    def test_setupDogfightOneAndTwoCards(self):
        simulator = DogfightSimulator("1", "1,1", Animations())
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
        simulator = DogfightSimulator("1,1,1", "1,1,1,1", Animations())
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
        simulator = DogfightSimulator("1,1,1,1,1", "1,1,1,1,1,1", Animations())
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
        simulator = DogfightSimulator("1,1,1,1,1,1,1", "1,1,1,1,1,1,1,1,1,1,1,1", Animations())
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

    def test_playCardWhenCycledWorksProperly(self):
        #id 3 has initialize: cycle 1 card
        #id 10 has when this card is cycled, play it in your leftmost open gunner slot
        simulator = DogfightSimulator("1,1,1,1,1,1,1", "7,10,1,1,1,1,1,1", Animations())
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
        animations = Animations()
        simulator = DogfightSimulator("1,1,1,1,1,1,1", "0,0,0,0,0,0,0,0", animations)
        simulator.simulateDogfight()#fight called inside here
        assert "p,1w,0,0" in animations.animationsList

    def test_fightHasCorrectWinnerInGuaranteedPlayerTwoWin(self):
        animations = Animations()
        simulator = DogfightSimulator("0,0,0,0,0,0,0,0", "1,1,1,1,1,1,1", animations)
        simulator.simulateDogfight()#fight called inside here
        assert "s,2w,0,0" in animations.animationsList

    def test_fightTiesInGuaranteedTie(self):
        animations = Animations()
        simulator = DogfightSimulator("0,0,0,0,0,0,0,0", "0,0,0,0,0,0,0,0", animations)
        simulator.simulateDogfight()#fight called inside here
        assert "b,ft,0,0" in animations.animationsList