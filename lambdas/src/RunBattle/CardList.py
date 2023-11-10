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
        
    def activateEffectsFor(self, timing, player, card):
        for effect in self.effects:
            if (effect.timing == timing):
                self.activateEffect(effect, player, card)
                
    def activateEffect(self, effect, player, card):
        match effect.effectType:
            case EffectType.POWERCOUNTER:
                self.activatePowerCounterEffect(effect, player, card)
            case EffectType.CYCLE:
                self.activateCycleEffect(effect, player)
                
    def activatePowerCounterEffect(self, effect, player, card):
        match effect.target:
            case Target.SELF:
                self.powerCounters += effect.intValue
                Animations.animationsList.append(player.playerIdentifier + ",pow," + str(effect.intValue) + "," + str(self.teamSlot))
            case Target.ALL:
                for card in player.team:
                    if (card != None):
                        card.powerCounters += effect.intValue
                        Animations.animationsList.append(player.playerIdentifier + ",pow," + str(effect.intValue) + "," + str(card.teamSlot))
                        
    def activateCycleEffect(self, effect, player):
        for iteration in range(0, effect.intValue):
            player.cycleCard();
                
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