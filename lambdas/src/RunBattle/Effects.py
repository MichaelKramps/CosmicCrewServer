from enum import Enum
import copy

class Timing(Enum):
    INITIALIZE = 1
    WINNER = 2 #when this card wins
    LOSER = 3 #when this card loses
    AFTERWINNING = 4 #when this card wins, after it has been replaced by another gunner
    ANYWINNER = 5 #when any friendly fighter wins
    ANYLOSER = 6 #when any friendly fighter loses
    SIGNINGBONUS = 7
    ONDRAW = 8
    WHENCYCLED = 9
    ONOPPONENTDRAW = 10
    POWERCHANGE = 11
    ONANYINITIALIZE = 12
    ONFRIENDLYPOWERCOUNTER = 13
    
class EffectType(Enum):
    POWERCOUNTER = 1
    SCRAP = 2
    CYCLE = 3
    PLAYCARD = 4
    DESTROYCARD = 5
    SETFIGHTERDESTINATION = 6
    SETOPPOSINGFIGHTERDESTINATION = 7
    REPLACEFIGHTER = 8
    
class Target(Enum):
    SELF = 1
    LEFTMOST = 2
    RIGHTMOST = 3
    RANDOM = 4
    CYCLEDCARD = 5
    ALL = 6
    NONE = 7
    BOTHPLAYERS = 8
    OPPOSINGFIGHTER = 9
    DECK = 10
    DISCARD = 11
    REPLACEMENTFIGHTER = 12

class TargetFilter(Enum):
    NOFILTER = 1
    ATHYR = 2
    LEANOR = 3
    RANCE = 4
    HASPOWERCOUNTER = 5
    LOWESTPOWER = 6

class Condition(Enum):
    NONE = 1
    ACTIVECARDHASPOWER = 2
    TEAMHASATLEASTXGUNNERS = 3
    REPLACINGWINNER = 4
    SELFHASPOWER = 5

class IntValue(Enum):
    CURRENTPOWERCOUNTERS = 1
    
class Effect:
    def __init__(self, timing, effectType, target, intValue):
        self.timing = timing
        self.effectType = effectType
        self.target = target
        self.condition = Condition.NONE
        self.intValue = intValue
        self.conditionValue = 0
        self.targetFilter = TargetFilter.NOFILTER
        self.originalFireXMoreTimes = -1
        self.fireXMoreTimes = -1 #means it fires forever
        
    def getAnimationCode(self, player, card):
        animationCode = player.playerIdentifier + ","
        animationCode += self.getEffectCode()
        animationCode += str(self.intValue) + ","
        animationCode += str(card.teamSlot)
        return animationCode
        
    def getEffectCode(self):
        match self.effectType:
            case EffectType.POWERCOUNTER:
                return "pow,"
            case EffectType.SCRAP:
                return "scr,"
            case EffectType.DESTROYCARD:
                return "des,"
            
    def addCondition(self, condition, conditionValue):
        self.condition = condition
        self.conditionValue = conditionValue
        return self
    
    def addTargetFilter(self, filter):
        self.targetFilter = filter
        return self
    
    def addNumberTimesToFire(self, numberTimesToFire):
        self.originalFireXMoreTimes = numberTimesToFire
        self.fireXMoreTimes = numberTimesToFire
        return self
    
    def fireEffect(self):
        if self.fireXMoreTimes > 0:
            self.fireXMoreTimes -= 1

    def resetEffect(self):
        if (self.originalFireXMoreTimes > 0):
            self.fireXMoreTimes = self.originalFireXMoreTimes

    @staticmethod
    def withName(name):
        effect = effects[name]
        if (effect.originalFireXMoreTimes != -1):
            return Effect(effect.timing, effect.effectType, effect.target, effect.intValue).addCondition(effect.condition, effect.conditionValue).addTargetFilter(effect.targetFilter).addNumberTimesToFire(effect.originalFireXMoreTimes)
        else:
            return effect

    
effects = {
    "initializeOnePowerCounterSelf": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1),
    "initializeTwoPowerCounterSelf": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 2),
    "initializeThreePowerCounterSelf": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 3),
    "initializeOnePowerCounterAll": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1),
    "initializeCycleOne": Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.NONE, 1),
    "onDrawOnePowerCounterSelf": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, 1),
    "onDrawOnePowerCounterLeftmost": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.LEFTMOST, 1),
    "whenCycledPlayCard": Effect(Timing.WHENCYCLED, EffectType.PLAYCARD, Target.SELF, 1),
    "onDrawOnePowerCounterAllIfCardIsOnePower": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDHASPOWER, 1),
    "loserCycleThree": Effect(Timing.LOSER, EffectType.CYCLE, Target.NONE, 3),
    "initializeOnePowerCounterAllAthyr": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1).addTargetFilter(TargetFilter.ATHYR),
    "initializeRemoveOnePowerCounterLeftmost": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.LEFTMOST, -1).addTargetFilter(TargetFilter.HASPOWERCOUNTER),
    "bodySnatcherEffect": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, Target.CYCLEDCARD).addNumberTimesToFire(1),
    "signingBonusScrapOne": Effect(Timing.SIGNINGBONUS, EffectType.SCRAP, Target.NONE, 1),
    "signingBonusScrapThree": Effect(Timing.SIGNINGBONUS, EffectType.SCRAP, Target.NONE, 3),
    "anyWinnerCycleOne": Effect(Timing.ANYWINNER, EffectType.CYCLE, Target.NONE, 1),
    "anyLoserCycleOne": Effect(Timing.ANYLOSER, EffectType.CYCLE, Target.NONE, 1),
    "initializeBothCycleOne": Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.BOTHPLAYERS, 1),
    "onOpponentDrawPowerCounterLeftmost": Effect(Timing.ONOPPONENTDRAW, EffectType.POWERCOUNTER, Target.LEFTMOST, 1),
    "onOpponentDrawPowerCounterRightmost": Effect(Timing.ONOPPONENTDRAW, EffectType.POWERCOUNTER, Target.RIGHTMOST, 1),
    "initializeFourPowerCountersSelfIfFourFighters": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 4).addCondition(Condition.TEAMHASATLEASTXGUNNERS, 4),
    "initializeTwoPowerCountersRandomLeanor": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.RANDOM, 2).addTargetFilter(TargetFilter.LEANOR),
    "initializeReplaceWinnerTwoPowerCountersAll": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 2).addCondition(Condition.REPLACINGWINNER, 0),
    "destroyIfPowerTen": Effect(Timing.POWERCHANGE, EffectType.DESTROYCARD, Target.SELF, 0).addCondition(Condition.SELFHASPOWER, 10),
    "onAnyInitializeOnePowerCounterSelf": Effect(Timing.ONANYINITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1),
    "sparkyTombManEffect": Effect(Timing.LOSER, EffectType.SETOPPOSINGFIGHTERDESTINATION, Target.DISCARD, 0),
    "loserPutBackInDeck": Effect(Timing.LOSER, EffectType.SETFIGHTERDESTINATION, Target.DECK, 0),
    "transferPowerCountersToReplacement": Effect(Timing.AFTERWINNING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, IntValue.CURRENTPOWERCOUNTERS),
    "powerCounterSelfOnTeammatePowerCounter": Effect(Timing.ONFRIENDLYPOWERCOUNTER, EffectType.POWERCOUNTER, Target.SELF, 1),
    "loserReplaceFighterLowestInDiscard": Effect(Timing.LOSER, EffectType.REPLACEFIGHTER, Target.DISCARD, 0).addTargetFilter(TargetFilter.LOWESTPOWER)
}