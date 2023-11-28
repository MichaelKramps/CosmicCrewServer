from Effects import Effect
from Effects import EffectType
from Effects import Target
from Effects import Condition
from Effects import TargetFilter
from enum import Enum

class Civilization(Enum):
    NONE = 1
    ATHYR = 2
    LEANOR = 3
    RANCE = 4

class Card:
    def __init__(self, name, id, power, effects, animations):
        self.id = id
        self.name = name
        self.power = power
        self.powerCounters = 0
        self.teamSlot = 0
        self.effects = effects
        self.civilization = Civilization.NONE
        self.animations = animations
        
    def activateEffectsFor(self, timing, player):
        for effect in self.effects:
            if (effect.timing == timing and self.conditionIsMet(effect, player)):
                self.activateEffect(effect, player)

    def conditionIsMet(self, effect, player):
        if effect.fireXMoreTimes == 0:
            return False
        match effect.condition:
            case Condition.NONE:
                return True
            case Condition.ACTIVECARDHASPOWER:
                if (player.activeCard.power == effect.conditionValue):
                    return True
                return False
        return True
            
                
    def activateEffect(self, effect, player):
        match effect.effectType:
            case EffectType.POWERCOUNTER:
                self.activatePowerCounterEffect(effect, player)
            case EffectType.CYCLE:
                self.activateCycleEffect(effect, player)
            case EffectType.PLAYCARD:
                self.activatePlayCardEffect(effect, player)
        effect.fireEffect()
            
                
    def activatePowerCounterEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                if (effect.intValue == Target.CYCLEDCARD):
                    self.powerCounters += player.activeCard.power
                    self.animations.addCodeFrom(player, effect, player.activeCard.power, self.teamSlot)
                else:
                    self.powerCounters += effect.intValue
                    self.animations.addCodeFrom(player, effect, effect.intValue, self.teamSlot)
            case Target.ALL:
                for card in player.team:
                    if (card != None and card.passesFilter(effect)):
                        card.powerCounters += effect.intValue
                        self.animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
            case Target.LEFTMOST:
                for card in player.team:
                    if (card != None and card.passesFilter(effect)):
                        card.powerCounters += effect.intValue
                        self.animations.addCodeFrom(player, effect, effect.intValue, card.teamSlot)
                        break
            case Target.RIGHTMOST:
                for card in reversed(player.team):
                    if (card != None and card.passesFilter(effect)):
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

    def passesFilter(self, effect):
        match effect.targetFilter:
            case TargetFilter.NOFILTER:
                return True
            case TargetFilter.ATHYR:
                return self.civilization == Civilization.ATHYR
            case TargetFilter.LEANOR:
                return self.civilization == Civilization.RANCE
            case TargetFilter.RANCE:
                return self.civilization == Civilization.LEANOR
            case TargetFilter.HASPOWERCOUNTER:
                return self.powerCounters > 0
        return True
                
    def clear(self):
        self.powerCounters = 0
        self.teamSlot = 0
        for effect in self.effects:
            effect.resetEffect()

    def addCivilizationFromInfo(self, cardInfo):
        self.civilization = Card.determineCivilization(cardInfo)
        return self
    
    def addCivilization(self, civilization):
        self.civilization = civilization
        return self

    @staticmethod
    def withId(id, animations):
        cardInfo = cardList[id]
        effects = []
        for effectName in cardInfo["effectNames"]:
            effects.append(Effect.withName(effectName))
        return Card(cardInfo["name"], cardInfo["id"], cardInfo["power"], effects, animations).addCivilizationFromInfo(cardInfo)
    
    @staticmethod
    def determineCivilization(cardInfo):
        match cardInfo["civilization"]:
            case "none":
                return Civilization.NONE
            case "athyr":
                return Civilization.ATHYR
            case "leanor":
                return Civilization.LEANOR
            case "rance":
                return Civilization.RANCE
        return Civilization.NONE

cardList = [
    {"name": "Baby Gunner", "id": 0, "power": 1, "effectNames": [], "civilization": "none"},
    {"name": "Teenage Gunner", "id": 1, "power": 2, "effectNames": [], "civilization": "none"},
    {"name": "Adult Gunner", "id": 2, "power": 3, "effectNames": [], "civilization": "none"},
    {"name": "CPU Teller", "id": 3, "power": 4, "effectNames": ["initializeOnePowerCounterSelf"], "civilization": "athyr"},
    {"name": "CPU Lender", "id": 4, "power": 3, "effectNames": ["initializeTwoPowerCounterSelf"], "civilization": "athyr"},
    {"name": "CPU Banker", "id": 5, "power": 2, "effectNames": ["initializeThreePowerCounterSelf"], "civilization": "athyr"},
    {"name": "Support Specialist", "id": 6,"power":  1, "effectNames": ["initializeOnePowerCounterAll"], "civilization": "none"},
    {"name": "Athyr Biker", "id": 7, "power": 3, "effectNames": ["initializeCycleOne"], "civilization": "athyr"},
    {"name": "Kip Ardor", "id": 8, "power": 1, "effectNames": ["onDrawOnePowerCounterSelf"], "civilization": "athyr"},
    {"name": "Klara Cobblestone", "id": 9, "power": 1, "effectNames": ["onDrawOnePowerCounterLeftmost"], "civilization": "athyr"},
    {"name": "Tadej, Unleashed", "id": 10, "power": 6, "effectNames": ["whenCycledPlayCard"], "civilization": "athyr"},
    {"name": "Drone Papa", "id": 11, "power": 3, "effectNames": ["onDrawOnePowerCounterAllIfCardIsOnePower"], "civilization": "athyr"},
    {"name": "Sepp Stepper", "id": 12, "power": 3, "effectNames": ["loserCycleThree"], "civilization": "athyr"},
    {"name": "Long Barreller", "id": 13, "power": 2, "effectNames": ["initializeOnePowerCounterAllAthyr"], "civilization": "athyr"},
    {"name": "Fixer Upper", "id": 14, "power": 7, "effectNames": ["initializeRemoveOnePowerCounterLeftmost"], "civilization": "athyr"},
    {"name": "Body Snatcher", "id": 15, "power": 2, "effectNames": ["initializeCycleOne", "bodySnatcherEffect"], "civilization": "athyr"}
    #{"name": "Garbage Collector", "id": 16, "power": 4, "effectNames": ["signingBonusScrapOne"], "civilization": "athyr"},
    #{"name": "Scrathyr", "id": 17, "power": 2, "effectNames": ["signingBonusScrapThree"], "civilization": "athyr"},
    #{"name": "Shop Owner", "id": 18, "power": 2, "effectNames": ["gunnerFightsCycleOne"], "civilization": "athyr"},
    #{"name": "Tandem Biker", "id": 19, "power": 5, "effectNames": ["initializeBothCycleOne"], "civilization": "athyr"},
    #{"name": "Jonas, Revived", "id": 20, "power": 3, "effectNames": ["discardCycledCards"], "civilization": "athyr"},
]