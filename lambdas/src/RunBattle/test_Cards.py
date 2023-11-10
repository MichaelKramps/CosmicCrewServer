from Cards import Card
from Effects import Effect
from Effects import effects
from Effects import Timing
from Effects import EffectType
from Effects import Target
from Animations import Animations
from Player import Player
import random
import unittest

class Test_CardClass(unittest.TestCase):

    def test_setsId(self):
        card = Card("p", 1, 1, [])
        assert card.id == 1

    def test_setsName(self):
        card = Card("p", 1, 1, [])
        assert card.name == "p"

    def test_setsPower(self):
        card = Card("p", 1, 1, [])
        assert card.power == 1

    def test_setsPowerCountersToZero(self):
        card = Card("p", 1, 1, [])
        assert card.powerCounters == 0

    def test_setTeamSlotToZero(self):
        card = Card("p", 1, 1, [])
        assert card.powerCounters == 0

    def test_setEffects(self):
        effectsList = [effects["initializeOnePowerCounterSelf"]]
        card = Card("p", 1, 1, effectsList)
        assert card.effects == effectsList

    def test_activatesSelfPowerCounterEffects(self):
        player = Player("0", "p")
        numberPowerCounters = random.randint(1,10)
        timing = random.choice(list(Timing))
        selfPowerCounterEffect = Effect(timing, EffectType.POWERCOUNTER, Target.SELF, numberPowerCounters)
        cardWithEffect = Card("test", 0, 0, [selfPowerCounterEffect])
        cardWithEffect.teamSlot = random.randint(1,5)
        cardWithEffect.activateEffectsFor(timing, player)
        assert cardWithEffect.powerCounters == numberPowerCounters
        animationString = player.playerIdentifier + ",pow," + str(numberPowerCounters) + "," + str(cardWithEffect.teamSlot)
        assert animationString in Animations.animationsList
