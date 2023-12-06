from Cards import Card
from Cards import Civilization
from Effects import Effect
from Effects import effects
from Effects import Timing
from Effects import EffectType
from Effects import Target
from Effects import TargetFilter
from Effects import Condition
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
        timing = random.choice(list(Timing))
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
        animations = Animations();
        numberPowerCounters = random.randint(1,10)
        timing = random.choice(list(Timing))
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
        timing = random.choice(list(Timing))
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
        timing = random.choice(list(Timing))
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
        timing = random.choice(list(Timing))
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
        timing = random.choice(list(Timing))
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
        timing = random.choice(list(Timing))
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
        indexOfWinningGunner = player.gunnerWins()
        player.activateGunnerWinsEffects(indexOfWinningGunner)
        assert player.deck[0].effects[1].fireXMoreTimes == 1

    def test_anyWinnerEffectsTrigger(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerValue = random.randint(1,10)
        anyWinnerEffect = Effect(Timing.ANYWINNER, EffectType.POWERCOUNTER, Target.SELF, powerValue)
        player.team = [Card("test", 0, 0, [anyWinnerEffect], animations), Card("test", 0, powerValue, [], animations), None, None, None, None]
        player.currentRoll = 2
        indexOfWinningGunner = player.gunnerWins()
        player.activateGunnerWinsEffects(indexOfWinningGunner)
        assert player.team[0].powerCounters == powerValue

    def test_anyLoserEffectsTrigger(self):
        animations = Animations()
        player = Player("0", "p", animations)
        powerValue = random.randint(1,10)
        anyWinnerEffect = Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.SELF, powerValue)
        player.team = [Card("test", 0, 0, [anyWinnerEffect], animations), Card("test", 0, powerValue, [], animations), None, None, None, None]
        player.currentRoll = 2
        losingGunner = player.gunnerLoses()
        player.activateGunnerLosesEffects(losingGunner)
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
        loser = player1.gunnerLoses()
        winner = player2.gunnerWins()
        player1.activateGunnerLosesEffects(loser)
        player2.activateGunnerWinsEffects(winner)
        assert len(player2.discard) == 1
        assert player2.discard[0] == testCard
        assert player1.fighterDestination == FighterDestination.DISCARD
        assert player2.fighterDestination == FighterDestination.DISCARD