from Effects import effects
from Effects import EffectType
from Effects import Target

class Card:
    def __init__(self, name, id, power, effects, animations):
        self.id = id
        self.name = name
        self.power = power
        self.powerCounters = 0
        self.teamSlot = 0
        self.effects = effects
        self.animations = animations
        
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
            case EffectType.PLAYCARD:
                self.activatePlayCardEffect(effect, player)
                
    def activatePowerCounterEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                self.powerCounters += effect.intValue
                self.animations.addCodeFrom(player, effect, effect.intValue, self.teamSlot)
            case Target.ALL:
                for card in player.team:
                    if (card != None):
                        card.powerCounters += effect.intValue
                        self.animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
            case Target.LEFTMOST:
                for card in player.team:
                    if (card != None):
                        card.powerCounters += effect.intValue
                        self.animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
                        break
            case Target.RIGHTMOST:
                for card in reversed(player.team):
                    if (card != None):
                        card.powerCounters += effect.intValue
                        self.animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
                        break
            case Target.RANDOM:
                randomRoll = player.rollDie()
                randomCard = player.gunnerFromRoll()
                randomCard.powerCounters += effect.intValue
                self.animations.addCodeFrom(player, effect, effect.intValue, randomCard.teamSlot)
                        
    def activateCycleEffect(self, effect, player):
        for iteration in range(0, effect.intValue):
            player.cycleCard()

    def activatePlayCardEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                if (player.leftmostOpenTeamSlot() > 0):
                    player.playCard(player.leftmostOpenTeamSlot())
                
    def clear(self):
        self.powerCounters = 0
        self.teamSlot = 0

    @staticmethod
    def getCardWithId(id, animations):
        cardInfo = cardList[id]
        return Card(cardInfo["name"], cardInfo["id"], cardInfo["power"], cardInfo["effects"], animations)

cardList = [
    {"name": "Baby Gunner", "id": 0, "power": 1, "effects": []},
    {"name": "Teenage Gunner", "id": 1, "power": 2, "effects": []},
    {"name": "Adult Gunner", "id": 2, "power": 3, "effects": []},
    {"name": "CPU Teller", "id": 3, "power": 4, "effects": [effects["initializeOnePowerCounterSelf"]]},
    {"name": "CPU Lender", "id": 4, "power": 3, "effects": [effects["initializeTwoPowerCounterSelf"]]},
    {"name": "CPU Banker", "id": 5, "power": 2, "effects": [effects["initializeThreePowerCounterSelf"]]},
    {"name": "Support Specialist", "id": 6,"power":  1, "effects": [effects["initializeOnePowerCounterAll"]]},
    {"name": "Athyr Biker", "id": 7, "power": 3, "effects": [effects["initializeCycleOne"]]},
    {"name": "Kip Ardor", "id": 8, "power": 1, "effects": [effects["onDrawOnePowerCounterSelf"]]},
    {"name": "Klara Cobblestone", "id": 9, "power": 1, "effects": [effects["onDrawOnePowerCounterLeftmost"]]},
    {"name": "Tadej, Unleashed", "id": 10, "power": 6, "effects": [effects["whenCycledPlayCard"]]}
]