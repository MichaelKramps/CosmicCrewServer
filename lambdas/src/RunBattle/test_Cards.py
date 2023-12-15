from Cards import Card
from Cards import Civilization
from Effects import Effect
from Effects import effects
from Effects import Timing
from Effects import EffectType
from Effects import Target
from Effects import TargetFilter
from Effects import Condition
from Effects import IntValue
from Animations import Animations
from Player import Player
from Player import FighterDestination
import random
import copy
import unittest

class Test_Cards(unittest.TestCase):

    def test_setsId(self):
        card = Card("p", 1, 1, [], Animations())
        assert card.id == 1

    def test_setsName(self):
        card = Card("p", 1, 1, [], Animations())
        assert card.name == "p"

    def test_setsPower(self):
        card = Card("p", 1, 1, [], Animations())
        assert card.power == 1

    def test_setsPowerCountersToZero(self):
        card = Card("p", 1, 1, [], Animations())
        assert card.powerCounters == 0

    def test_setTeamSlotToZero(self):
        card = Card("p", 1, 1, [], Animations())
        assert card.powerCounters == 0

    def test_setEffects(self):
        effectsList = [Effect.withName("initializeOnePowerCounterSelf")]
        card = Card("p", 1, 1, effectsList, Animations())
        assert card.effects == effectsList

    def test_activatesSelfPowerCounterEffects(self):
        animations = Animations()
        player = Player("0", "p", animations)
        numberPowerCounters = random.randint(1,10)
        timing = Timing.LOSER
        selfPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [selfPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == numberPowerCounters
        animationString = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithEffect.teamSlot)
        assert animationString in animations.animationsList

    def test_supportsMultipleEffectActivations(self):
        animations = Animations()
        player = Player("0", "p", animations)
        numberPowerCounters1 = random.randint(1,10)
        numberPowerCounters2 = random.randint(1,10)
        timing = Timing.INITIALIZE
        selfPowerCounterEffect1 = Effect(timing, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters1)
        selfPowerCounterEffect2 = Effect(timing, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters2)
        cardWithEffect = Card("test", 0, 0, [selfPowerCounterEffect1, selfPowerCounterEffect2], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == numberPowerCounters1 + numberPowerCounters2
        animationString1 = player.playerIdentifier + ",pow," + str(numberPowerCounters1) + "," + str(cardWithEffect.teamSlot)
        animationString2 = player.playerIdentifier + ",pow," + str(numberPowerCounters1) + "," + str(cardWithEffect.teamSlot)
        assert animationString1 in animations.animationsList
        assert animationString2 in animations.animationsList

    def test_activatesALLPowerCounterEffects(self):
        animations = Animations()
        numberPowerCounters = random.randint(1,10)
        timing = Timing.INITIALIZE
        allPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.ALL, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [allPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        cardWithoutEffect1 = Card("test", 0, 0, [], animations)
        cardWithoutEffect1.teamSlot = random.randint(1,10000)
        cardWithoutEffect2 = Card("test", 0, 0, [], animations)
        cardWithoutEffect2.teamSlot = random.randint(1,10000)
        player = Player("0", "test", animations)
        player.team = [cardWithEffect, cardWithoutEffect1, None, None, cardWithoutEffect2, None]
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == numberPowerCounters
        assert cardWithoutEffect1.powerCounters == numberPowerCounters
        assert cardWithoutEffect2.powerCounters == numberPowerCounters
        animationString1 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithEffect.teamSlot)
        animationString2 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithoutEffect1.teamSlot)
        animationString3 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithoutEffect2.teamSlot)
        assert animationString1 in animations.animationsList
        assert animationString2 in animations.animationsList
        assert animationString3 in animations.animationsList

    def test_activatesLEFTMOSTPowerCounterEffects(self):
        animations = Animations();
        numberPowerCounters = random.randint(1,10)
        timing = Timing.INITIALIZE
        leftmostPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.LEFTMOST, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [leftmostPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        leftmostCard = Card("test", 0, 0, [], animations)
        leftmostCard.teamSlot = random.randint(1,10000)
        rightmostCard = Card("test", 0, 0, [], animations)
        rightmostCard.teamSlot = random.randint(1,10000)
        player = Player("0", "test", animations)
        player.team = [None, leftmostCard, cardWithEffect, None, rightmostCard, None]
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == 0
        assert leftmostCard.powerCounters == numberPowerCounters
        assert rightmostCard.powerCounters == 0
        animationString = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(leftmostCard.teamSlot)
        assert animationString in animations.animationsList

    def test_activatesRIGHTMOSTPowerCounterEffects(self):
        animations = Animations();
        numberPowerCounters = random.randint(1,10)
        timing = Timing.INITIALIZE
        rightmostPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.RIGHTMOST, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [rightmostPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        leftmostCard = Card("test", 0, 0, [], animations)
        leftmostCard.teamSlot = random.randint(1,10000)
        rightmostCard = Card("test", 0, 0, [], animations)
        rightmostCard.teamSlot = random.randint(1,10000)
        player = Player("0", "test", animations)
        player.team = [None, leftmostCard, cardWithEffect, None, rightmostCard, None]
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == 0
        assert leftmostCard.powerCounters == 0
        assert rightmostCard.powerCounters == numberPowerCounters
        animationString = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(rightmostCard.teamSlot)
        assert animationString in animations.animationsList

    def test_activatesRANDOMPowerCounterEffects(self):
        animations = Animations();
        numberPowerCounters = random.randint(1,10)
        timing = Timing.INITIALIZE
        randomPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.RANDOM, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [randomPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        leftmostCard = Card("test", 0, 0, [], animations)
        leftmostCard.teamSlot = random.randint(1,10000)
        rightmostCard = Card("test", 0, 0, [], animations)
        rightmostCard.teamSlot = random.randint(1,10000)
        player = Player("0", "test", animations)
        player.team = [None, leftmostCard, cardWithEffect, None, rightmostCard, None]
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == numberPowerCounters or leftmostCard.powerCounters == numberPowerCounters or rightmostCard.powerCounters == numberPowerCounters
        animationString1 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithEffect.teamSlot)
        animationString2 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(leftmostCard.teamSlot)
        animationString3 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(rightmostCard.teamSlot)
        assert animationString1 in animations.animationsList or animationString2 in animations.animationsList or animationString3 in animations.animationsList

    def test_activatesRANDOMPowerCounterEffectsWithFilter(self):
        animations = Animations()
        numberPowerCounters = random.randint(1,10)
        timing = Timing.INITIALIZE
        randomPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.RANDOM, numberPowerCounters).addTargetFilter(TargetFilter.LEANOR)
        cardWithEffect = Card("test", 0, 0, [randomPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        leftmostCard = Card("test", 0, 0, [], animations)
        leftmostCard.teamSlot = random.randint(1,10000)
        rightmostCard = Card("test", 0, 0, [], animations).addCivilization(Civilization.LEANOR)
        rightmostCard.teamSlot = random.randint(1,10000)
        player = Player("0", "test", animations)
        player.team = [None, leftmostCard, cardWithEffect, None, rightmostCard, None]
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == 0 and leftmostCard.powerCounters == 0 and rightmostCard.powerCounters == numberPowerCounters
        animationString1 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithEffect.teamSlot)
        animationString2 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(leftmostCard.teamSlot)
        animationString3 = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(rightmostCard.teamSlot)
        assert animationString1 not in animations.animationsList and animationString2 not in animations.animationsList and animationString3 in animations.animationsList

    def test_cycleEffect(self):
        animations = Animations();
        player = Player("0", "p", animations)
        numberToCycle = random.randint(1,10)
        timing = Timing.INITIALIZE
        selfPowerCounterEffect = Effect(timing, EffectType.CYCLE, Target.NONE, numberToCycle)
        cardWithEffect = Card("test", 0, 0, [selfPowerCounterEffect], animations)
        testDeck = [
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
            Card("test", 0, 0, [], animations),
        ]
        cardThatShouldBeOnTop = testDeck[numberToCycle]
        player.deck = testDeck
        cardWithEffect.activateEffectsFor(timing, player)
        assert player.deck[0] == cardThatShouldBeOnTop
        animationString1 = player.playerIdentifier + ",dws,1,0"
        animationString2 = player.playerIdentifier + ",uns,1,0"
        assert animationString1 in animations.animationsList
        assert animationString2 in animations.animationsList

    def test_conditionActiveCardHasPower(self):
        animations = Animations();
        player = Player("0", "p", animations)
        conditionValue = random.randint(1,10)
        effectWithCondition = Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDHASPOWER, conditionValue)
        player.team = [Card("test", 0, 0, [effectWithCondition], animations), Card("test", 0, 0, [], animations), None, None, None, None]
        player.deck = [Card("test", 0, conditionValue, [], animations)]
        player.drawCard()
        assert player.team[0].powerCounters == 1
        assert player.team[1].powerCounters == 1


    def test_clearRemovesPowerCountersAndDeckSlot(self):
        card = Card("test", 1, 1, [], Animations())
        card.powerCounters = 3
        card.teamSlot = 3
        card.clear()
        assert card.powerCounters == 0
        assert card.teamSlot == 0

    def test_bodySnatcherEffect(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerValue = random.randint(1,10)
        player.team = [None, None, None, None, None, None]
        player.deck = [Card("test", 0, 0, [Effect.withName("initializeCycleOne"), Effect.withName("bodySnatcherEffect")], animations), Card("test", 0, powerValue, [], animations)]
        player.drawAndPlayCard(1)
        assert player.team[0].powerCounters == powerValue
        assert animations.codesAppearInOrder(["p,dws,1,0", "p,pow," + str(powerValue) + ",1", "p,uns,1,0"])
        player.drawAndPlayCard(2)
        assert player.team[0].powerCounters == powerValue

    def test_xTimesEffectsReset(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerValue = random.randint(1,10)
        player.team = [None, None, None, None, None, None]
        player.deck = [Card("test", 0, 0, [Effect.withName("initializeCycleOne"), Effect.withName("bodySnatcherEffect")], animations), Card("test", 0, powerValue, [], animations)]
        player.drawAndPlayCard(1)
        assert player.team[0].powerCounters == powerValue
        assert animations.codesAppearInOrder(["p,dws,1,0", "p,pow," + str(powerValue) + ",1", "p,uns,1,0"])
        player.currentRoll = 1
        player.gunnerWins()
        player.activateGunnerWinsEffects()
        assert player.deck[0].effects[1].fireXMoreTimes == 1

    def test_anyWinnerEffectsTrigger(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerValue = random.randint(1,10)
        anyWinnerEffect = Effect(Timing.ANYWINNER, EffectType.POWERCOUNTER, Target.SELF, powerValue)
        player.team = [Card("test", 0, 0, [anyWinnerEffect], animations), Card("test", 0, powerValue, [], animations), None, None, None, None]
        player.currentRoll = 2
        player.gunnerWins()
        player.activateGunnerWinsEffects()
        assert player.team[0].powerCounters == powerValue

    def test_anyLoserEffectsTrigger(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerValue = random.randint(1,10)
        anyWinnerEffect = Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.SELF, powerValue)
        player.team = [Card("test", 0, 0, [anyWinnerEffect], animations), Card("test", 0, powerValue, [], animations), None, None, None, None]
        player.currentRoll = 2
        player.gunnerLoses()
        player.activateGunnerLosesEffects()
        assert player.team[0].powerCounters == powerValue

    def test_bothPlayersCycleOne(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        player2 = Player("1", "s", animations)
        player1.addOpponent(player2)
        player2.addOpponent(player1)
        bothCycleEffect = Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.BOTHPLAYERS, 1)
        testCard1 = Card("test", 0, 0, [], animations)
        testCard2 = Card("test", 0, 0, [], animations)
        player1.deck = [Card("test", 0, 0, [bothCycleEffect], animations), Card("test", 0, 0, [], animations), testCard1]
        player2.deck = [Card("test", 0, 0, [], animations), testCard2]
        player1.team = [None, None, None, None, None, None]
        player1.drawAndPlayCard(1)
        assert player1.deck[0] == testCard1
        assert player2.deck[0] == testCard2

    def test_opponentDrawsCard(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        player2 = Player("1", "s", animations)
        player1.addOpponent(player2)
        player2.addOpponent(player1)
        opponentDrawsEffect = Effect(Timing.ONOPPONENTDRAW, EffectType.POWERCOUNTER, Target.SELF, 1)
        testCard = Card("test", 0, 0, [opponentDrawsEffect], animations)
        testCard.teamSlot = 1
        player2.deck = [Card("test", 0, 0, [], animations)]
        player1.team = [testCard, None, None, None, None, None]
        player2.drawCard()
        assert testCard.powerCounters == 1
        assert animations.codesAppearInOrder(["p,pow,1,1"])

    def test_numberCardsOnTeamConditionDoesntActivateEffectCorrectly(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerCounterEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1).addCondition(Condition.TEAMHASATLEASTXGUNNERS, 3)
        testCard = Card("test", 0, 0, [powerCounterEffect], animations)
        testCard.teamSlot = 2
        player.deck = [testCard]
        player.team = [Card("test", 0, 0, [], animations), None, None, None, None, None]
        player.drawAndPlayCard(2)
        assert testCard.powerCounters == 0

    def test_numberCardsOnTeamConditionActivatesEffectCorrectly(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerCounterEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1).addCondition(Condition.TEAMHASATLEASTXGUNNERS, 3)
        testCard = Card("test", 0, 0, [powerCounterEffect], animations)
        testCard.teamSlot = 2
        player.deck = [testCard]
        player.team = [Card("test", 0, 0, [], animations), None, Card("test", 0, 0, [], animations), None, None, None]
        player.drawAndPlayCard(2)
        assert testCard.powerCounters == 1
        assert animations.codesAppearInOrder(["p,pow,1,2"])

    def test_replacingWinningFighterEffectTriggers(self):
        animations = Animations()
        player = Player("0", "p", animations)
        player.currentRoll = 1
        replaceWinnerEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1).addCondition(Condition.REPLACINGWINNER, 0)
        testCard = Card("test", 0, 0, [replaceWinnerEffect], animations)
        testCard.teamSlot = 1
        player.deck = [testCard]
        player.team = [Card("test", 0, 0, [], animations), None, Card("test", 0, 0, [], animations), None, None, None]
        winningFighter = player.gunnerWins()
        player.activateGunnerWinsEffects(winningFighter)
        assert testCard.powerCounters == 1
        assert animations.codesAppearInOrder(["p,pow,1,1"])

    def test_replacingWinningFighterEffectTriggers(self):
        animations = Animations()
        player = Player("0", "p", animations)
        replaceWinnerEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1).addCondition(Condition.REPLACINGWINNER, 0)
        testCard = Card("test", 0, 0, [replaceWinnerEffect], animations)
        testCard.teamSlot = 1
        player.deck = [testCard]
        player.team = [Card("test", 0, 0, [], animations), None, Card("test", 0, 0, [], animations), None, None, None]
        player.drawAndPlayCard(2)
        assert testCard.powerCounters == 0
        assert not animations.codesAppearInOrder(["p,pow,1,1"])

    def test_destroyCardEffectWorks(self):
        animations = Animations()
        player = Player("0", "p", animations)
        destroyCardEffect = Effect(Timing.INITIALIZE, EffectType.DESTROYCARD, Target.SELF, 0)
        testCard = Card("test", 0, 0, [destroyCardEffect], animations)
        testCard.teamSlot = 1
        player.deck = [testCard]
        player.drawAndPlayCard(1)
        assert player.team[0] == None
        assert player.discard[0] == testCard
        assert animations.codesAppearInOrder(["p,des,0,1"])

    def test_destroyCardEffectWorks(self):
        animations = Animations()
        player = Player("0", "p", animations)
        destroyCardEffect = Effect(Timing.POWERCHANGE, EffectType.DESTROYCARD, Target.SELF, 0).addCondition(Condition.SELFHASPOWER, 2)
        powerCounterEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1)
        testCard = Card("test", 0, 1, [destroyCardEffect], animations)
        testCard.teamSlot = 1
        player.deck = [Card("test", 0, 0, [powerCounterEffect], animations)]
        player.team = [testCard, None, None, None, None, None]
        player.drawAndPlayCard(2)
        assert player.team[0] == None
        assert player.discard[0] == testCard
        assert animations.codesAppearInOrder(["p,des,0,1"])

    def test_onAnyInitializeTimingWorks(self):
        animations = Animations()
        player = Player("0", "p", animations)
        anyInitializeEffect = Effect(Timing.ONANYINITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1)
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 0)
        testCard = Card("test", 0, 0, [anyInitializeEffect], animations)
        testCard.teamSlot = 1
        player.deck = [Card("test", 0, 0, [initializeEffect], animations)]
        player.team = [testCard, None, None, None, None, None]
        player.drawAndPlayCard(2)
        assert player.team[0].powerCounters == 1

    def test_onAnyInitializeTimingWorksWithOpponentInitialize(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        player2 = Player("1", "s", animations)
        player1.addOpponent(player2)
        player2.addOpponent(player1)
        anyInitializeEffect = Effect(Timing.ONANYINITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1)
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 0)
        testCard = Card("test", 0, 0, [anyInitializeEffect], animations)
        testCard.teamSlot = 1
        player2.deck = [Card("test", 0, 0, [initializeEffect], animations)]
        player1.team = [testCard, None, None, None, None, None]
        player2.drawAndPlayCard(1)
        assert testCard.powerCounters == 1
        assert animations.codesAppearInOrder(["p,pow,1,1"])

    def test_sparkyTombEffectWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        player2 = Player("1", "s", animations)
        player1.addOpponent(player2)
        player2.addOpponent(player1)
        sparkTombEffect = Effect(Timing.LOSER, EffectType.SETOPPOSINGFIGHTERDESTINATION, Target.DISCARD, 0)
        testCard = Card("test", 0, 0, [], animations)
        player1.currentRoll = 1
        player2.currentRoll = 1
        player1.team = [Card("test", 0, 0, [sparkTombEffect], animations), None, None, None, None, None]
        player2.team = [testCard, None, None, None, None, None]
        player1.gunnerLoses()
        player2.gunnerWins()
        player1.activateGunnerLosesEffects()
        player2.activateGunnerWinsEffects()
        assert len(player2.discard) == 1
        assert player2.discard[0] == testCard
        assert player1.fighterDestination == FighterDestination.DISCARD
        assert player2.fighterDestination == FighterDestination.DISCARD

    def test_loseAndGoToBottomOfDeckEffectWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        loseDeckEffect = Effect(Timing.LOSER, EffectType.SETFIGHTERDESTINATION, Target.DECK, 0)
        testCard = Card("test", 0, 0, [loseDeckEffect], animations)
        player1.currentRoll = 1
        player1.team = [testCard, None, None, None, None, None]
        player1.gunnerLoses()
        player1.activateGunnerLosesEffects()
        assert len(player1.discard) == 0
        assert player1.fighterDestination == FighterDestination.DECK
        assert testCard in player1.deck

    def test_transferPowerCountersEffectWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        transferCountersEffect = Effect(Timing.AFTERWINNING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, IntValue.CURRENTPOWERCOUNTERS)
        transferCard = Card("test", 0, 0, [transferCountersEffect], animations)
        transferCard.teamSlot = 1
        numberPowerCounters = random.randint(1,10)
        transferCard.powerCounters = numberPowerCounters
        testCard = Card("test", 0, 0, [], animations)
        player1.team = [transferCard, None, None, None, None, None]
        player1.deck = [testCard]
        player1.gunnerWins()
        player1.activateGunnerWinsEffects()
        assert testCard.powerCounters == numberPowerCounters
        assert animations.codesAppearInOrder(["p,p,1,0", "p,pow," + str(numberPowerCounters) + ",1"])

    def test_onFriendlyPowerCounterEffectWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        onPowerCounterEffect = Effect(Timing.ONFRIENDLYPOWERCOUNTER, EffectType.POWERCOUNTER, Target.SELF, 1)
        testCard = Card("test", 0, 0, [onPowerCounterEffect], animations)
        numberPowerCounters = random.randint(1,10)
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        initializeCard = Card("test", 0, 0, [initializeEffect], animations)
        player1.team = [testCard, None, None, None, None, None]
        player1.deck = [initializeCard, initializeCard]
        player1.drawAndPlayCard(2)
        player1.drawAndPlayCard(3)
        assert testCard.powerCounters == 2

    def test_onFriendlyPowerCounterIsntInfinite(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        onPowerCounterEffect = Effect(Timing.ONFRIENDLYPOWERCOUNTER, EffectType.POWERCOUNTER, Target.SELF, 1)
        testCard = Card("test", 0, 0, [onPowerCounterEffect], animations)
        numberPowerCounters = random.randint(1,10)
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        initializeCard = Card("test", 0, 0, [initializeEffect, onPowerCounterEffect], animations)
        player1.team = [testCard, None, None, None, None, None]
        player1.deck = [initializeCard, initializeCard]
        player1.drawAndPlayCard(2)
        player1.drawAndPlayCard(3)
        assert testCard.powerCounters == 2

    def test_onFriendlyPowerCounterDoesntFireWhenRemovingCounter(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        onPowerCounterEffect = Effect(Timing.ONFRIENDLYPOWERCOUNTER, EffectType.POWERCOUNTER, Target.SELF, 1)
        testCard = Card("test", 0, 0, [onPowerCounterEffect], animations)
        numberPowerCounters = -1
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        initializeCard = Card("test", 0, 0, [initializeEffect, onPowerCounterEffect], animations)
        player1.team = [testCard, None, None, None, None, None]
        player1.deck = [initializeCard, initializeCard]
        player1.drawAndPlayCard(2)
        player1.drawAndPlayCard(3)
        assert testCard.powerCounters == 0

    def test_onFriendlyPowerCounterCantTriggerItself(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        onPowerCounterEffect = Effect(Timing.ONFRIENDLYPOWERCOUNTER, EffectType.POWERCOUNTER, Target.SELF, 1)
        testCard = Card("test", 0, 0, [onPowerCounterEffect], animations)
        numberPowerCounters = 1
        initializeEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        initializeCard1 = Card("test", 0, 0, [initializeEffect, onPowerCounterEffect], animations)
        initializeCard1.teamSlot = 2
        initializeCard2 = Card("test", 0, 0, [initializeEffect, onPowerCounterEffect], animations)
        initializeCard2.teamSlot = 3
        player1.team = [testCard, None, None, None, None, None]
        player1.deck = [initializeCard1, initializeCard2]
        player1.drawAndPlayCard(2)
        player1.drawAndPlayCard(3)
        assert testCard.powerCounters == 2
        assert player1.team[1].powerCounters == 2
        assert player1.team[2].powerCounters == 1

    def test_leanorWinsPowerUpLeanorFighters(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        leanorWinsEffect = Effect(Timing.ANYWINNER, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDISLEANOR, 1).addTargetFilter(TargetFilter.LEANOR)
        testCard = Card("test", 0, 0, [leanorWinsEffect], animations)
        testCard.civilization = Civilization.LEANOR
        leanorCard = Card("test", 0, 0, [], animations)
        leanorCard.civilization = Civilization.LEANOR
        leanorCard2 = Card("test", 0, 0, [], animations)
        leanorCard2.civilization = Civilization.LEANOR
        nonLeanorCard = Card("test", 0, 0, [], animations)
        player1.team = [testCard, nonLeanorCard, leanorCard, leanorCard2, None, None]
        player1.currentRoll = 4
        player1.gunnerWins()
        player1.activateGunnerWinsEffects()
        assert testCard.powerCounters == 1
        assert nonLeanorCard.powerCounters == 0
        assert leanorCard.powerCounters == 1

    def test_leanorWinsPowerUpLeanorFightersNonLeanorWinner(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        leanorWinsEffect = Effect(Timing.ANYWINNER, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDISLEANOR, 1).addTargetFilter(TargetFilter.LEANOR)
        testCard = Card("test", 0, 0, [leanorWinsEffect], animations)
        testCard.civilization = Civilization.LEANOR
        leanorCard = Card("test", 0, 0, [], animations)
        leanorCard.civilization = Civilization.LEANOR
        leanorCard2 = Card("test", 0, 0, [], animations)
        leanorCard2.civilization = Civilization.LEANOR
        nonLeanorCard = Card("test", 0, 0, [], animations)
        player1.team = [testCard, nonLeanorCard, leanorCard, leanorCard2, None, None]
        player1.currentRoll = 2
        player1.gunnerWins()
        player1.activateGunnerWinsEffects()
        assert testCard.powerCounters == 0
        assert leanorCard.powerCounters == 0
        assert leanorCard2.powerCounters == 0

    def test_EnemyHasFighterWithPowerConditionWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        player2 = Player("0", "s", animations)
        player1.addOpponent(player2)
        numberPowerCounters = random.randint(1,10)
        powerConditionEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters).addCondition(Condition.ENEMYHASFIGHTERWITHPOWER, 10)
        testCard = Card("test", 0, 0, [powerConditionEffect], animations)
        player2.team = [None, Card("test", 0, 10, [], animations), None, None, None, None]
        player1.deck = [testCard]
        player1.drawAndPlayCard(1)
        assert testCard.powerCounters == numberPowerCounters

    def test_EnemyHasFighterWithPowerConditionWorksNegation(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        player2 = Player("0", "s", animations)
        player1.addOpponent(player2)
        numberPowerCounters = random.randint(1,10)
        powerConditionEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters).addCondition(Condition.ENEMYHASFIGHTERWITHPOWER, 10)
        testCard = Card("test", 0, 0, [powerConditionEffect], animations)
        player2.team = [None, Card("test", 0, 9, [], animations), None, None, None, None]
        player1.deck = [testCard]
        player1.drawAndPlayCard(1)
        assert testCard.powerCounters == 0

    def test_removeAllTeamPowerCountersWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        removeAllEffect = Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, IntValue.REMOVEALLPOWERCOUNTERS)
        effectCard = Card("test", 0, 0, [removeAllEffect], animations)
        testCard0 = Card("test", 0, 0, [], animations)
        testCard1 = Card("test", 0, 0, [], animations)
        testCard1.powerCounters = 1
        testCard2 = Card("test", 0, 0, [], animations)
        testCard2.powerCounters = 2
        testCard3 = Card("test", 0, 0, [], animations)
        testCard3.powerCounters = 3
        player1.team = [testCard1, testCard2, testCard3, testCard0, None, None]
        player1.deck = [effectCard]
        player1.drawAndPlayCard(5)
        assert effectCard.powerCounters == 0
        assert testCard0.powerCounters == 0
        assert testCard1.powerCounters == 0
        assert testCard2.powerCounters == 0
        assert testCard3.powerCounters == 0

    def test_replaceEffectWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        replaceEffect = Effect(Timing.LOSER, EffectType.REPLACEFIGHTER, Target.SELF, 0)
        effectCard = Card("effectCard", 0, 0, [replaceEffect], animations)
        effectCard.teamSlot = 2
        testCard = Card("test", 0, 0, [], animations)
        player1.team = [None, effectCard, None, None, None, None]
        player1.deck = [testCard]
        player1.currentRoll = 2
        player1.gunnerLoses()
        player1.activateGunnerLosesEffects()
        assert player1.team[1] == testCard
        assert effectCard in player1.discard

    def test_afterLosingTimingWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        replaceEffect = Effect(Timing.LOSER, EffectType.REPLACEFIGHTER, Target.SELF, 0)
        numberPowerCounters = random.randint(1,10)
        afterlosingEffect = Effect(Timing.AFTERLOSING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, numberPowerCounters)
        effectCard = Card("effectCard", 0, 0, [replaceEffect, afterlosingEffect], animations)
        effectCard.teamSlot = 2
        testCard = Card("test", 0, 0, [], animations)
        player1.team = [None, effectCard, None, None, None, None]
        player1.deck = [testCard]
        player1.currentRoll = 2
        player1.gunnerLoses()
        player1.activateGunnerLosesEffects()
        assert player1.team[1] == testCard
        assert testCard.powerCounters == numberPowerCounters
        assert effectCard in player1.discard

    def test_doublePowerCountersWorks(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        doubleEffect = Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.ALL, IntValue.DOUBLEPOWERCOUNTERS)
        effectCard = Card("effectCard", 0, 0, [doubleEffect], animations)
        effectCard.teamSlot = 2
        testCard0 = Card("test", 0, 0, [], animations)
        testCard1 = Card("test", 0, 0, [], animations)
        testCard1.powerCounters = 1
        testCard2 = Card("test", 0, 0, [], animations)
        testCard2.powerCounters = 2
        testCard3 = Card("test", 0, 0, [], animations)
        testCard3.powerCounters = 3
        player1.team = [testCard0, effectCard, testCard1, testCard2, testCard3, None]
        player1.currentRoll = 2
        player1.gunnerLoses()
        player1.activateGunnerLosesEffects()
        assert testCard0.powerCounters == 0
        assert testCard1.powerCounters == 2
        assert testCard2.powerCounters == 4
        assert testCard3.powerCounters == 6

    def test_hapthorEffectsWork(self):
        animations = Animations()
        player1 = Player("0", "p", animations)
        hapthorEffect1 = Effect(Timing.ANYLOSER, EffectType.REPLACEFIGHTER, Target.CURRENTFIGHTER, 0)
        hapthorEffect2 = Effect(Timing.ANYLOSER, EffectType.REPLACEFIGHTER, Target.SELF, 0)
        loserEffect = Effect(Timing.LOSER, EffectType.REPLACEFIGHTER, Target.SELF, 0)
        hapthorCard = Card("hapthor", 0, 0, [hapthorEffect1, hapthorEffect2], animations)
        hapthorCard.teamSlot = 2
        replacementCard1 = Card("replacement1", 0, 0, [], animations)
        replacementCard2 = Card("replacement2", 0, 0, [], animations)
        replacementCard3 = Card("replacement3", 0, 0, [], animations)
        loserCard = Card("loser", 0, 0, [loserEffect], animations)
        loserCard.teamSlot = 1
        player1.team = [loserCard, hapthorCard, None, None, None, None]
        player1.deck = [replacementCard1, replacementCard2, replacementCard3]
        player1.currentRoll = 1
        player1.gunnerLoses()
        player1.activateGunnerLosesEffects()
        player1.printTeam()
        assert player1.team[0] == replacementCard1
        assert player1.team[1] == replacementCard2