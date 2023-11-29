from Animations import Animations
from Effects import Effect
from Effects import Timing
from Effects import EffectType
from Effects import Target
from Effects import TargetFilter
from Effects import effects
from Cards import Card
from Cards import Civilization
from Player import Player
import random
import unittest

class Test_Player(unittest.TestCase):
    def test_setsPlayerIdentifier(self):
        player = Player("1", "p", Animations())
        assert player.playerIdentifier == "p"

    def test_setsDeck(self):
        player = Player("1,2,3", "p", Animations())
        assert len(player.deck) == 3

    def test_setsTeamBlank(self):
        player = Player("1", "p", Animations())
        assert player.team != None
        assert len(player.team) == 6

    def test_setsDiscard(self):
        player = Player("1", "p", Animations())
        assert player.discard != None
        assert len(player.discard) == 0

    def test_currentRoll(self):
        player = Player("1", "p", Animations())
        assert player.currentRoll == 0

    def test_rollDieRollsSixSidedDie(self):
        player = Player("1", "p", Animations())
        player.rollDie()
        assert player.currentRoll > 0
        assert player.currentRoll <= 6

    def test_drawCardGetsTopCardOfDeck(self):
        player = Player("1", "p", Animations())
        cardToDraw = player.deck[0]
        player.drawCard()
        assert player.activeCard == cardToDraw

    def test_drawFromEmptyDeckWritesAnimationCode(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.deck = []
        player.drawCard()
        assert "p,ded,0,0" in animations.animationsList
        assert len(animations.animationsList) == 1

    def test_drawFromDeckWritesAnimationCode(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.drawCard()
        assert "p,dws,1,0" in animations.animationsList
        assert len(animations.animationsList) == 1

    def test_drawCardTriggersDrawCardEffectsOfTeam(self):
        animations = Animations()
        player = Player("1", "p", animations)
        numberPowerCounters = random.randint(1,10)
        drawCardTimingEffect = Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [drawCardTimingEffect], animations)
        slot = random.randint(1,10000)
        cardWithEffect.teamSlot = slot
        player.team = [None, None, cardWithEffect, None, None, None]
        player.drawCard()
        assert cardWithEffect.powerCounters == numberPowerCounters
        assert "p,pow," + str(numberPowerCounters) + "," + str(slot) in animations.animationsList

    def test_putCardOnBottomOfDeckClearsCard(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        cardToTest.powerCounters = 4
        cardToTest.teamSlot = 5
        player.deck = [cardToTest]
        player.drawCard()
        player.putCardOnBottomOfDeck()
        assert cardToTest.powerCounters == 0
        assert cardToTest.teamSlot == 0

    def test_putCardOnBottomOfDeckPutsCardOnBottomOfDeck(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        player.deck = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.drawCard()
        player.putCardOnBottomOfDeck()
        assert player.deck[0] != cardToTest
        assert player.deck[1] != cardToTest
        assert player.deck[2] == cardToTest

    def test_playCardPlaysCardInTheRightSpot(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert player.team[2] == cardToTest

    def test_playCardSetsTeamSlot(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert cardToTest.teamSlot == 3

    def test_playCardAddsAnimationCode(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert "p,p,3,0" in animations.animationsList

    def test_playCardActivatesINITIALIZEEffect(self):
        animations = Animations()
        player = Player("1", "p", animations)
        numberPowerCounters = random.randint(1,10)
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardToTest = Card("test", 0, 0, [initializeEffect], animations)
        player.deck = [cardToTest]
        player.drawCard()
        player.playCard(3)
        assert cardToTest.powerCounters == numberPowerCounters

    def test_cycleCardMovesTopCardToBottom(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        player.deck = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.cycleCard()
        assert player.deck[0] != cardToTest
        assert player.deck[1] != cardToTest
        assert player.deck[2] == cardToTest

    def test_cycleCardAddsAnimationCodes(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardToTest = Card("test", 0, 0, [], animations)
        player.deck = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.cycleCard()
        assert animations.codesAppearInOrder(["p,dws,1,0", "p,uns,1,0"])

    def test_cycleCardPutsDrawCardAnimationCodesInBetweenDrawCodes(self):
        animations = Animations()
        player = Player("1", "p", animations)
        numberPowerCounters = random.randint(1,10)
        onDrawEffect = Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardToTest = Card("test", 0, 0, [onDrawEffect], animations)
        cardToTest.teamSlot = 3
        player.team = [None, None, cardToTest, None, None, None]
        player.deck = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.cycleCard()
        assert animations.codesAppearInOrder(["p,dws,1,0", "p,pow," + str(numberPowerCounters) + ",3", "p,uns,1,0"])

    def test_indexFromRollOneDirectHit(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = random.randint(1,6)
        player.team = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        assert player.gunnerIndexFromRoll() == player.currentRoll - 1

    def test_indexFromRollSingleMiss(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = 3
        player.team = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), None, None, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        assert player.gunnerIndexFromRoll() == 4

    def test_indexFromRollRolloverSix(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = 3
        player.team = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), None, None, None, None]
        assert player.gunnerIndexFromRoll() == 0

    def test_gunnerFromRollReturnsCorrectGunner(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.rollDie()
        player.team = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), None, None, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        assert player.gunnerFromRoll() == player.team[player.gunnerIndexFromRoll()]

    def test_gunnerWinsClearsWinningGunner(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [], animations)
        cardToTest.powerCounters = 4
        player.team = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.gunnerWins()
        assert cardToTest.powerCounters == 0

    def test_gunnerWinsDoesntReplaceIfEmptyDeck(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.deck = []
        player.currentRoll = 1
        player.team = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.gunnerWins()
        assert player.team[0] == None

    def test_gunnerWinsReplacesGunner(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cardInDeck = Card("test", 0, 0, [], animations)
        player.deck = [cardInDeck]
        player.currentRoll = 1
        player.team = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        indexOfWinningGunner = player.gunnerWins()
        player.activateGunnerWinsEffects(indexOfWinningGunner)
        assert player.team[0] == cardInDeck

    def test_gunnerWinsPutsWinningGunnerOnBottomOfDeck(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.deck = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.currentRoll = 1
        winningCard = Card("test", 0, 0, [], animations)
        player.team = [winningCard, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        indexOfWinningGunner = player.gunnerWins()
        player.activateGunnerWinsEffects(indexOfWinningGunner)
        assert player.deck[1] == winningCard

    def test_gunnerLosesClearsLosingGunner(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [], animations)
        cardToTest.powerCounters = 4
        player.team = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.gunnerLoses()
        assert cardToTest.powerCounters == 0

    def test_gunnerLosesAddsLosingGunnerToDiscard(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [], animations)
        player.team = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.gunnerLoses()
        assert cardToTest in player.discard

    def test_gunnerLosesRemovesLosingGunnerFromTeam(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.currentRoll = 1
        cardToTest = Card("test", 0, 0, [], animations)
        player.team = [cardToTest, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        player.gunnerLoses()
        assert player.team[0] == None

    def test_stillAliveTrueIfGunnerOnTeam(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.team = [None, None, None, None, Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations)]
        assert player.stillAlive() == True     

    def test_stillAliveFalseIfNoGunnersOnTeam(self):
        animations = Animations()
        player = Player("1", "p", animations)
        player.team = [None, None, None, None, None, None]
        assert player.stillAlive() == False

    def test_playCardWhenCycledWorks(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cycleEffectCard = Card("cycle", 0, 1, [Effect.withName("initializeCycleOne")], animations)
        playWhenCycledCard = Card("playWhenCycled", 1, 1, [Effect.withName("whenCycledPlayCard")], animations)
        player.deck = [cycleEffectCard, playWhenCycledCard]
        player.drawAndPlayCard(1)
        assert player.team == [cycleEffectCard, playWhenCycledCard, None, None, None, None]

    def test_canCycleMoreThanOneCard(self):
        animations = Animations()
        player = Player("1", "p", animations)
        cycleEffect = Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.NONE, 3)
        testCard = Card("test", 0, 0, [], animations)
        player.deck = [Card("test", 0, 0, [cycleEffect], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), testCard]
        player.drawAndPlayCard(1)
        assert player.deck[0] == testCard

    def test_canActivateLoserEffects(self):
        animations = Animations()
        player = Player("1", "p", animations)
        loserEffect = Effect(Timing.LOSER, EffectType.CYCLE, Target.NONE, 3)
        testCard = Card("test", 0, 0, [], animations)
        player.team = [Card("test", 0, 0, [loserEffect], animations), None, None, None, None, Card("test", 0, 0, [], animations)]
        player.deck = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), testCard]
        player.currentRoll = 1
        losingGunner = player.gunnerLoses()
        player.activateGunnerLosesEffects(losingGunner)
        assert player.deck[0] == testCard

    def test_canActivateWinnerEffects(self):
        animations = Animations()
        player = Player("1", "p", animations)
        winnerEffect = Effect(Timing.WINNER, EffectType.CYCLE, Target.NONE, 3)
        testCard = Card("test", 0, 0, [], animations)
        player.team = [Card("test", 0, 0, [winnerEffect], animations), None, None, None, None, Card("test", 0, 0, [], animations)]
        player.deck = [Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), Card("test", 0, 0, [], animations), testCard]
        player.currentRoll = 1
        indexOfWinningGunner = player.gunnerWins()
        player.activateGunnerWinsEffects(indexOfWinningGunner)
        assert player.team[0] == testCard

    def test_targetFilterWorks(self):
        animations = Animations()
        player = Player("1", "p", animations)
        filteredEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1).addTargetFilter(TargetFilter.ATHYR)
        player.team = [Card("test", 0, 0, [], animations).addCivilization(Civilization.ATHYR), None, None, None, None, Card("test", 0, 0, [], animations)]
        player.deck = [Card("test", 0, 0, [filteredEffect], animations).addCivilization(Civilization.LEANOR)]
        player.drawAndPlayCard(2)
        assert player.team[0].powerCounters == 1
        assert player.team[1].powerCounters == 0
        assert player.team[5].powerCounters == 0