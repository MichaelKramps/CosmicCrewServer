from Effects import Effect
from Effects import EffectType
from Effects import Target
from Effects import Timing
from Effects import Condition
from Effects import TargetFilter
from Effects import IntValue
from enum import Enum
import random

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
        self.replacingWinner = False
        self.isReplacement = False
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
            case Condition.TEAMHASATLEASTXGUNNERS:
                fightersOnTeam = 0
                for slot in player.team:
                    if slot != None:
                        fightersOnTeam += 1
                return fightersOnTeam >= effect.conditionValue
            case Condition.REPLACINGWINNER:
                return self.replacingWinner
            case Condition.SELFHASPOWER:
                return self.getTotalPower() >= effect.conditionValue
            case Condition.ACTIVECARDISLEANOR:
                return player.currentFighter.civilization == Civilization.LEANOR
            case Condition.ACTIVECARDISATHYR:
                return player.currentFighter.civilization == Civilization.ATHYR
            case Condition.ACTIVECARDISRANCE:
                return player.currentFighter.civilization == Civilization.RANCE
            case Condition.ENEMYHASFIGHTERWITHPOWER:
                return player.opponent.hasFighterWithPower(effect.conditionValue)
            case Condition.OPPONENTHASMOREFIGHTERS:
                return player.numberFightersRemaining() < player.opponent.numberFightersRemaining()
        return True
            
                
    def activateEffect(self, effect, player):
        match effect.effectType:
            case EffectType.POWERCOUNTER:
                self.activatePowerCounterEffect(effect, player)
            case EffectType.CYCLE:
                self.activateCycleEffect(effect, player)
            case EffectType.PLAYCARD:
                self.activatePlayCardEffect(effect, player)
            case EffectType.DESTROYCARD:
                self.activateDestroyCardEffect(effect, player)
            case EffectType.SETFIGHTERDESTINATION:
                self.activateSetFighterDestinationEffect(effect, player)
            case EffectType.SETOPPOSINGFIGHTERDESTINATION:
                self.activateSetOpposingFighterDestinationEffect(effect, player)
            case EffectType.REPLACEFIGHTER:
                self.activateReplaceFighterEffect(effect, player)
        effect.fireEffect()
        if effect.timing == Timing.INITIALIZE:
            player.activateEffectsForTeam(Timing.ONANYINITIALIZE)
            player.activateEffectsForOpponentTeam(Timing.ONANYINITIALIZE)
            
                
    def activatePowerCounterEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                if (effect.intValue == IntValue.CYCLEDCARD):
                    powerCountersToAdd = self.determinePowerCountersToAdd(effect, self, player)
                    if powerCountersToAdd != 0:
                        self.powerCounters += powerCountersToAdd
                        self.animations.addCodeFrom(player, effect, powerCountersToAdd, self.teamSlot)
                        self.activateEffectsFor(Timing.POWERCHANGE, player)
                        self.attemptOnFriendlyEffect(player, effect, self.teamSlot, powerCountersToAdd)
                else:
                    powerCountersToAdd = self.determinePowerCountersToAdd(effect, self, player)
                    if powerCountersToAdd != 0:
                        self.powerCounters += powerCountersToAdd
                        self.animations.addCodeFrom(player, effect, powerCountersToAdd, self.teamSlot)
                        self.activateEffectsFor(Timing.POWERCHANGE, player)
                        self.attemptOnFriendlyEffect(player, effect, self.teamSlot, powerCountersToAdd)
            case Target.ALL:
                for card in player.team:
                    if (card != None and card.passesFilter(effect)):
                        powerCountersToAdd = self.determinePowerCountersToAdd(effect, card, player)
                        if powerCountersToAdd != 0:
                            card.powerCounters += powerCountersToAdd
                            self.animations.addCodeFrom(player, effect, powerCountersToAdd, card.teamSlot)
                            card.activateEffectsFor(Timing.POWERCHANGE, player)
                            self.attemptOnFriendlyEffect(player, effect, card.teamSlot, powerCountersToAdd)
            case Target.LEFTMOST:
                for card in player.team:
                    if (card != None and card.passesFilter(effect)):
                        powerCountersToAdd = self.determinePowerCountersToAdd(effect, card, player)
                        if powerCountersToAdd != 0:
                            card.powerCounters += powerCountersToAdd
                            self.animations.addCodeFrom(player, effect, powerCountersToAdd, card.teamSlot)
                            card.activateEffectsFor(Timing.POWERCHANGE, player)
                            self.attemptOnFriendlyEffect(player, effect, card.teamSlot, powerCountersToAdd)
                        break
            case Target.RIGHTMOST:
                for card in reversed(player.team):
                    if (card != None and card.passesFilter(effect)):
                        powerCountersToAdd = self.determinePowerCountersToAdd(effect, card, player)
                        if powerCountersToAdd != 0:
                            card.powerCounters += powerCountersToAdd
                            self.animations.addCodeFrom(player, effect, powerCountersToAdd, card.teamSlot)
                            card.activateEffectsFor(Timing.POWERCHANGE, player)
                            self.attemptOnFriendlyEffect(player, effect, card.teamSlot, powerCountersToAdd)
                        break
            case Target.RANDOM:
                randomRoll = random.randint(1, 6)
                indexOfFighterToGiveEffect = player.gunnerIndexFromSlotWithFilter(randomRoll, effect)
                if indexOfFighterToGiveEffect != None:
                    randomCard = player.team[indexOfFighterToGiveEffect]
                    powerCountersToAdd = self.determinePowerCountersToAdd(effect, randomCard, player)
                    if powerCountersToAdd != 0:
                        randomCard.powerCounters += powerCountersToAdd
                        self.animations.addCodeFrom(player, effect, powerCountersToAdd, randomCard.teamSlot)
                        randomCard.activateEffectsFor(Timing.POWERCHANGE, player)
                        self.attemptOnFriendlyEffect(player, effect, randomCard.teamSlot, powerCountersToAdd)
            case Target.REPLACEMENTFIGHTER:
                powerCountersToAdd = self.determinePowerCountersToAdd(effect, self, player)
                replacementCard = player.team[self.teamSlot - 1]
                if (replacementCard != None and powerCountersToAdd != 0):
                    replacementCard.powerCounters += powerCountersToAdd
                    self.animations.addCodeFrom(player, effect, powerCountersToAdd, replacementCard.teamSlot)
                    replacementCard.activateEffectsFor(Timing.POWERCHANGE, player)
                    self.attemptOnFriendlyEffect(player, effect, replacementCard.teamSlot, powerCountersToAdd)

    def determinePowerCountersToAdd(self, effect, card, player):
        match effect.intValue:
            case IntValue.CURRENTPOWERCOUNTERS:
                return self.powerCounters
            case IntValue.REMOVEALLPOWERCOUNTERS:
                return 0 - card.powerCounters
            case IntValue.DOUBLEPOWERCOUNTERS:
                return card.powerCounters
            case IntValue.CYCLEDCARD:
                return player.activeCard.power
            case IntValue.POWEROFVICTOR:
                return player.opponent.currentFighter.getTotalPower()
        return effect.intValue
                        
    def activateCycleEffect(self, effect, player):
        for iteration in range(0, effect.intValue):
            player.cycleCard()
            if (effect.target == Target.BOTHPLAYERS):
                player.opponent.cycleCard()

    def activatePlayCardEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                if (player.leftmostOpenTeamSlot() > 0):
                    player.playCard(player.leftmostOpenTeamSlot())

    def activateDestroyCardEffect(self, effect, player):
        match effect.target:
            case Target.SELF:
                player.destroyCardFromEffect(self, effect)
            case Target.RANDOMENEMYFIGHTER:
                randomRoll = random.randint(1, 6)
                indexOfFighterToGiveEffect = player.opponent.gunnerIndexFromSlotWithFilter(randomRoll, effect)
                player.opponent.destroyCardFromEffect(player.opponent.team[indexOfFighterToGiveEffect], effect)

    def activateSetFighterDestinationEffect(self, effect, player):
        player.setFighterDestination(effect)

    def activateSetOpposingFighterDestinationEffect(self, effect, player):
        player.opponent.setFighterDestination(effect)

    def activateReplaceFighterEffect(self, effect, player):
        fighterToReplace = self
        match effect.target:
            case Target.SELF:
                fighterToReplace = self
            case Target.CURRENTFIGHTER:
                fighterToReplace = player.currentFighter
        player.replaceFighterEffect(fighterToReplace)
            

    def attemptOnFriendlyEffect(self, player, effect, teamSlot, powerCountersAdded):
        if (effect.timing != Timing.ONFRIENDLYPOWERCOUNTER and powerCountersAdded > 0): #prevents infinite power counter effect
            player.activateEffectsForTeammates(Timing.ONFRIENDLYPOWERCOUNTER, teamSlot)

    def passesFilter(self, effect):
        match effect.targetFilter:
            case TargetFilter.NOFILTER:
                return True
            case TargetFilter.ATHYR:
                return self.civilization == Civilization.ATHYR
            case TargetFilter.LEANOR:
                return self.civilization == Civilization.LEANOR
            case TargetFilter.RANCE:
                return self.civilization == Civilization.RANCE
            case TargetFilter.HASPOWERCOUNTER:
                return self.powerCounters > 0
        return True
                
    def clear(self):
        self.powerCounters = 0
        self.teamSlot = 0
        self.replacingWinner = False
        self.isReplacement = False
        for effect in self.effects:
            effect.resetEffect()

    def addCivilizationFromInfo(self, cardInfo):
        self.civilization = Card.determineCivilization(cardInfo)
        return self
    
    def addCivilization(self, civilization):
        self.civilization = civilization
        return self
    
    def getTotalPower(self):
        return self.power + self.powerCounters

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
    {"name": "Body Snatcher", "id": 15, "power": 2, "effectNames": ["initializeCycleOne", "bodySnatcherEffect"], "civilization": "athyr"},
    {"name": "Garbage Collector", "id": 16, "power": 4, "effectNames": ["signingBonusScrapOne"], "civilization": "athyr"},
    {"name": "Scrathyr", "id": 17, "power": 2, "effectNames": ["signingBonusScrapThree"], "civilization": "athyr"},
    {"name": "Shop Owner", "id": 18, "power": 2, "effectNames": ["anyWinnerCycleOne", "anyLoserCycleOne"], "civilization": "athyr"},
    {"name": "Tandem Biker", "id": 19, "power": 5, "effectNames": ["initializeBothCycleOne"], "civilization": "athyr"},
    {"name": "Jonas, Revived", "id": 20, "power": 3, "effectNames": ["onOpponentDrawPowerCounterLeftmost", "onOpponentDrawPowerCounterRightmost"], "civilization": "athyr"},
    {"name": "Extroverted Fighter", "id": 21, "power": 3, "effectNames": ["initializeFourPowerCountersSelfIfFourFighters"], "civilization": "leanor"},
    {"name": "Leanor Hype Man", "id": 22, "power": 3, "effectNames": ["initializeTwoPowerCountersRandomLeanor"], "civilization": "leanor"},
    {"name": "Shy Flyer", "id": 23, "power": 2, "effectNames": ["initializeReplaceWinnerTwoPowerCountersAll"], "civilization": "leanor"},
    {"name": "Supercharged Brawler", "id": 24, "power": 9, "effectNames": ["destroyIfPowerTen"], "civilization": "leanor"},
    {"name": "Fabiano, Starter Gun", "id": 25, "power": 4, "effectNames": ["onAnyInitializeOnePowerCounterSelf"], "civilization": "leanor"},
    {"name": "Sparky Sparky Tomb Man", "id": 26, "power": 3, "effectNames": ["sparkyTombManEffect"], "civilization": "leanor"},
    {"name": "Maxime, the Gifter", "id": 27, "power": 6, "effectNames": ["loserPutBackInDeck"], "civilization": "leanor"},
    {"name": "Sniper Patton", "id": 28, "power": 2, "effectNames": ["transferPowerCountersToReplacement"], "civilization": "leanor"},
    {"name": "General Gonto", "id": 29, "power": 1, "effectNames": ["powerCounterSelfOnTeammatePowerCounter"], "civilization": "leanor"},
    {"name": "Untrained Medic", "id": 30, "power": 3, "effectNames": ["anyLoserOnePowerCounterRandom"], "civilization": "leanor"},
    {"name": "Shak Shyarov", "id": 31, "power": 1, "effectNames": ["powerCounterAllLeanorWhenLeanorWins", "powerCounterAllLeanorWhenLeanorLoses"], "civilization": "leanor"},
    {"name": "Snake Eyes", "id": 32, "power": 2, "effectNames": ["initializeOnePowerCounterLeftmost", "initializeOnePowerCounterRightmost"], "civilization": "leanor"},
    {"name": "Alloysmith", "id": 33, "power": 3, "effectNames": ["winnerPowerCounterAll"], "civilization": "leanor"},
    {"name": "Vishy, the Valiant", "id": 34, "power": 2, "effectNames": ["anyWinnerTwoPowerCountersSelf", "anyLoserTwoPowerCountersSelf"], "civilization": "leanor"},
    {"name": "Flip Face", "id": 35, "power": 1, "effectNames": ["initializeTenPowerCountersIfOpponentHasTenPower"], "civilization": "leanor"},
    {"name": "Shooting Buddy", "id": 36, "power": 2, "effectNames": ["initializeOnePowerCounterAllFriendlyLeanor"], "civilization": "leanor"},
    {"name": "Shield Disruptor", "id": 37, "power": 10, "effectNames": ["initializeRemoveAllPowerCounters"], "civilization": "leanor"},
    {"name": "Disavowed Traitor", "id": 38, "power": 3, "effectNames": ["loserReplace"], "civilization": "rance"},
    {"name": "Weapon Grifter", "id": 39, "power": 8, "effectNames": ["loserReplace", "loserRemoveAllPowerCounters"], "civilization": "rance"},
    {"name": "Mechoward", "id": 40, "power": 1, "effectNames": ["loserReplace", "afterLosingTwoPowerCountersReplacement"], "civilization": "rance"},
    {"name": "Tampering Coroner", "id": 41, "power": 3, "effectNames": ["loserDoublePowerCountersAll"], "civilization": "rance"},
    {"name": "Hapthor, Everlasting", "id": 42, "power": 0, "effectNames": ["hapthorEffect", "destroyIfPowerOne"], "civilization": "rance"},
    {"name": "Wheel Whacker", "id": 43, "power": 2, "effectNames": ["loserReplace", "afterLosingOnePowerCounterReplacement"], "civilization": "rance"},
    {"name": "Auto Equalizer", "id": 44, "power": 1, "effectNames": ["loserSixPowerCountersRandom"], "civilization": "rance"},
    {"name": "Kamakaze Tech", "id": 45, "power": 0, "effectNames": ["loserKamakazeEffect"], "civilization": "rance"},
    {"name": "Minion Upgrader", "id": 46, "power": 3, "effectNames": ["anyLoserOnePowerCounterLeftmost", "anyLoserOnePowerCounterRightmost"], "civilization": "rance"},
    {"name": "Explosive Ally", "id": 47, "power": 4, "effectNames": ["loserTwoPowerCountersLeftmost", "loserTwoPowerCountersRightmost"], "civilization": "rance"},
    {"name": "Big Z Cannon", "id": 48, "power": 2, "effectNames": ["anyLoserThreePowerCountersSelf"], "civilization": "rance"},
    {"name": "Shaw, the Helpful", "id": 49, "power": 6, "effectNames": ["loserSixPowerCountersRightmost"], "civilization": "rance"},
    {"name": "Armor Burglar", "id": 50, "power": 4, "effectNames": ["anyLoserFourPowerCountersRandom"], "civilization": "rance"},
    {"name": "Rance Faithful", "id": 51, "power": 2, "effectNames": [], "civilization": "rance"},
    {"name": "Gun Thief", "id": 52, "power": 1, "effectNames": ["loserVictorPowerToRandom"], "civilization": "rance"},
    {"name": "Trash Electromagnet", "id": 53, "power": 3, "effectNames": ["afterWinningThreePowerCountersReplacement"], "civilization": "rance"},
    #{"name": "Name", "id": 54, "power": 2, "effectNames": [], "civilization": "rance"},
    #{"name": "Name", "id": 55, "power": 2, "effectNames": [], "civilization": "rance"},
]