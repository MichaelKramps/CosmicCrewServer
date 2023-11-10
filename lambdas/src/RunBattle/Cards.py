from Effects import effects
from Effects import EffectType
from Effects import Target
from Animations import Animations

class Card:
    def __init__(self, name, id, power, effects):
        self.id = id
        self.name = name
        self.power = power
        self.powerCounters = 0
        self.teamSlot = 0
        self.effects = effects
        
    def activateEffectsFor(self, timing, player):
        for effect in self.effects:
            if (effect.timing == timing):
                self.activateEffect(effect, player)
                
    def activateEffect(self, effect, player):
        match effect.effectType:
            case EffectType.POWERCOUNTER:
                self.activatePowerCounterEffect(effect, player)
            case EffectType.CYCLE:
                self.activateCycleEffect(effect, player)
                
    def activatePowerCounterEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                self.powerCounters += effect.intValue
                Animations.addCodeFrom(player, effect, effect.intValue, self.teamSlot)
            case Target.ALL:
                for card in player.team:
                    if (card != None):
                        card.powerCounters += effect.intValue
                        Animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
            case Target.LEFTMOST:
                for card in player.team:
                    if (card != None):
                        card.powerCounters += effect.intValue
                        Animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
                        break
            case Target.RIGHTMOST:
                for card in reversed(player.team):
                    if (card != None):
                        card.powerCounters += effect.intValue
                        Animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
                        break
            case Target.RANDOM:
                randomRoll = player.rollDie()
                randomCard = player.gunnerFromRoll()
                randomCard.powerCounters += effect.intValue
                Animations.addCodeFrom(player, effect, effect.intValue, randomCard.teamSlot)
                        
    def activateCycleEffect(self, effect, player):
        for iteration in range(0, effect.intValue):
            player.cycleCard()
                
    def clear(self):
        self.powerCounters = 0
        self.teamSlot = 0

cardList = [
    Card("Baby Gunner", 0, 1, []),
    Card("Teenage Gunner", 1, 2, []),
    Card("Adult Gunner", 2, 3, []),
    Card("CPU Teller", 3, 4, [effects["initializeOnePowerCounterSelf"]]),
    Card("CPU Lender", 4, 3, [effects["initializeTwoPowerCounterSelf"]]),
    Card("CPU Banker", 5, 2, [effects["initializeThreePowerCounterSelf"]]),
    Card("Support Specialist", 6, 1, [effects["initializeOnePowerCounterAll"]]),
    Card("Athyr Biker", 7, 3, [effects["initializeCycleOne"]]),
    Card("Kip Ardor", 8, 1, [effects["onDrawOnePowerCounterSelf"]])
]