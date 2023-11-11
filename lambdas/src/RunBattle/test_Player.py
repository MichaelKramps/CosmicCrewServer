from Animations import Animations
from Effects import Effect
from Effects import Timing
from Effects import EffectType
from Effects import Target
from Cards import Card
from Player import Player
import random
import unittest

class Test_Player(unittest.TestCase):
    def setUp(self):
        Animations.clearAnimations()

    def test_setsPlayerIdentifier(self):
        player = Player("1", "p")
        assert player.playerIdentifier == "p"

    def test_setsDeck(self):
        player = Player("1,2,3", "p")
        assert len(player.deck) == 3

    def test_setsTeamBlank(self):
        player = Player("1", "p")
        assert player.team != None
        assert len(player.team) == 6

    def test_setsDiscard(self):
        player = Player("1", "p")
        assert player.discard != None
        assert len(player.discard) == 0

    def test_currentRoll(self):
        player = Player("1", "p")
        assert player.currentRoll == 0

    def test_rollDieRollsSixSidedDie(self):
        player = Player("1", "p")
        player.rollDie()
        assert player.currentRoll > 0
        assert player.currentRoll <= 6

    def test_drawCardGetsTopCardOfDeck(self):
        player = Player("1", "p")
        cardToDraw = player.deck[0]
        player.drawCard()
        assert player.activeCard == cardToDraw

    def test_drawFromEmptyDeckWritesAnimationCode(self):
        player = Player("1", "p")
        player.deck = []
        player.drawCard()
        assert "p,ded,0,0" in Animations.animationsList
        assert len(Animations.animationsList) == 1

    def test_drawFromDeckWritesAnimationCode(self):
        player = Player("1", "p")
        player.drawCard()
        assert "p,dws,1,0" in Animations.animationsList
        assert len(Animations.animationsList) == 1

    def test_drawCardTriggersDrawCardEffectsOfTeam(self):
        player = Player("1", "p")
        numberPowerCounters = random.randint(1,10)
        drawCardTimingEffect = Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [drawCardTimingEffect])
        slot = random.randint(1,10000)
        cardWithEffect.teamSlot = slot
        player.team = [None, None, cardWithEffect, None, None, None]
        player.drawCard()
        assert cardWithEffect.powerCounters == numberPowerCounters
        assert "p,pow," + str(numberPowerCounters) + "," + str(slot) in Animations.animationsList

    def test_putCardOnBottomOfDeckClearsCard(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        cardToTest.powerCounters = 4
        cardToTest.teamSlot = 5
        player.deck = [cardToTest]
        player.drawCard()
        player.putCardOnBottomOfDeck()
        assert cardToTest.powerCounters == 0
        assert cardToTest.teamSlot == 0

    def test_putCardOnBottomOfDeckPutsCardOnBottomOfDeck(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        player.deck = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.drawCard()
        player.putCardOnBottomOfDeck()
        assert player.deck[0] != cardToTest
        assert player.deck[1] != cardToTest
        assert player.deck[2] == cardToTest

    def test_playCardPlaysCardInTheRightSpot(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert player.team[2] == cardToTest

    def test_playCardSetsTeamSlot(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert cardToTest.teamSlot == 3

    def test_playCardAddsAnimationCode(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert "p,p,3,0" in Animations.animationsList

    def test_playCardActivatesINITIALIZEEffect(self):
        player = Player("1", "p")
        numberPowerCounters = random.randint(1,10)
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardToTest = Card("test", 0, 0, [initializeEffect])
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert cardToTest.powerCounters == numberPowerCounters

    def test_cycleCardMovesTopCardToBottom(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        player.deck = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.cycleCard()
        assert player.deck[0] != cardToTest
        assert player.deck[1] != cardToTest
        assert player.deck[2] == cardToTest

    def test_cycleCardAddsAnimationCodes(self):
        player = Player("1", "p")
        cardToTest = Card("test", 0, 0, [])
        player.deck = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.cycleCard()
        assert Animations.codesAppearInOrder(["p,dws,1,0", "p,uns,1,0"])

    def test_cycleCardPutsDrawCardAnimationCodesInBetweenDrawCodes(self):
        player = Player("1", "p")
        numberPowerCounters = random.randint(1,10)
        onDrawEffect = Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardToTest = Card("test", 0, 0, [onDrawEffect])
        cardToTest.teamSlot = 3
        player.team = [None, None, cardToTest, None, None, None]
        player.deck = [Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.cycleCard()
        assert Animations.codesAppearInOrder(["p,dws,1,0", "p,pow," + str(numberPowerCounters) + ",3", "p,uns,1,0"])

    def test_indexFromRollOneDirectHit(self):
        player = Player("1", "p")
        player.currentRoll = random.randint(1,6)
        player.team = [Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        assert player.gunnerIndexFromRoll() == player.currentRoll - 1

    def test_indexFromRollSingleMiss(self):
        player = Player("1", "p")
        player.currentRoll = 3
        player.team = [Card("test", 0, 0, []), Card("test", 0, 0, []), None, None, Card("test", 0, 0, []), Card("test", 0, 0, [])]
        assert player.gunnerIndexFromRoll() == 4

    def test_indexFromRollRolloverSix(self):
        player = Player("1", "p")
        player.currentRoll = 3
        player.team = [Card("test", 0, 0, []), Card("test", 0, 0, []), None, None, None, None]
        assert player.gunnerIndexFromRoll() == 0

    def test_gunnerFromRollReturnsCorrectGunner(self):
        player = Player("1", "p")
        player.rollDie()
        player.team = [Card("test", 0, 0, []), Card("test", 0, 0, []), None, None, Card("test", 0, 0, []), Card("test", 0, 0, [])]
        assert player.gunnerFromRoll() == player.team[player.gunnerIndexFromRoll()]

    def test_gunnerWinsClearsWinningGunner(self):
        player = Player("1", "p")
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [])
        cardToTest.powerCounters = 4
        player.team = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerWins()
        assert cardToTest.powerCounters == 0

    def test_gunnerWinsDoesntReplaceIfEmptyDeck(self):
        player = Player("1", "p")
        player.deck = []
        player.currentRoll = 1
        player.team = [Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerWins()
        assert player.team[0] == None

    def test_gunnerWinsReplacesGunner(self):
        player = Player("1", "p")
        cardInDeck = Card("test", 0, 0, [])
        player.deck = [cardInDeck]
        player.currentRoll = 1
        player.team = [Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerWins()
        assert player.team[0] == cardInDeck

    def test_gunnerWinsPutsWinningGunnerOnBottomOfDeck(self):
        player = Player("1", "p")
        player.deck = [Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.currentRoll = 1
        winningCard = Card("test", 0, 0, [])
        player.team = [winningCard, Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerWins()
        assert player.deck[1] == winningCard

    def test_gunnerLosesClearsLosingGunner(self):
        player = Player("1", "p")
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [])
        cardToTest.powerCounters = 4
        player.team = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerLoses()
        assert cardToTest.powerCounters == 0

    def test_gunnerLosesAddsLosingGunnerToDiscard(self):
        player = Player("1", "p")
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [])
        player.team = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerLoses()
        assert cardToTest in player.discard

    def test_gunnerLosesRemovesLosingGunnerFromTeam(self):
        player = Player("1", "p")
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [])
        player.team = [cardToTest, Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, []), Card("test", 0, 0, [])]
        player.gunnerLoses()
        assert player.team[0] == None

    def test_stillAliveTrueIfGunnerOnTeam(self):
        player = Player("1", "p")
        player.team = [None, None, None, None, Card("test", 0, 0, []), Card("test", 0, 0, [])]
        assert player.stillAlive() == True     

    def test_stillAliveFalseIfNoGunnersOnTeam(self):
        player = Player("1", "p")
        player.team = [None, None, None, None, None, None]
        assert player.stillAlive() == False