from CardList import Card
from Effects import Effect
from Effects import effects
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