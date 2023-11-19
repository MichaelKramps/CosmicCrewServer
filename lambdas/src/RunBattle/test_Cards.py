from Cards import Card
from Effects import Effect
from Effects import effects
from Effects import Timing
from Effects import EffectType
from Effects import Target
from Animations import Animations
from Player import Player
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
        effectsList = [effects["initializeOnePowerCounterSelf"]]
        card = Card("p", 1, 1, effectsList, Animations())
        assert card.effects == effectsList

    def test_activatesSelfPowerCounterEffects(self):
        animations = Animations();
        player = Player("0", "p", animations)
        numberPowerCounters = random.randint(1,10)
        timing = random.choice(list(Timing))
        selfPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [selfPowerCounterEffect], animations)
        cardWithEffect.teamSlot = random.randint(1,10000)
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == numberPowerCounters
        animationString = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithEffect.teamSlot)
        assert animationString in animations.animationsList

    def test_supportsMultipleEffectActivations(self):
        animations = Animations();
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

    def test_clearRemovesPowerCountersAndDeckSlot(self):
        card = Card("test", 1, 1, [], Animations())
        card.powerCounters = 3
        card.teamSlot = 3
        card.clear()
        assert card.powerCounters == 0
        assert card.teamSlot == 0