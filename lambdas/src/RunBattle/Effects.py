from enum import Enum
import copy

class Timing(Enum):
    INITIALIZE = 1
    WINNER = 2 #when this card wins
    LOSER = 3 #when this card loses
    AFTERWINNING = 4 #when this card wins, after it has been replaced by another gunner
    AFTERLOSING = 5 #some effects replace the loser and will interact with the replacement
    ANYWINNER = 6 #when any friendly fighter wins
    ANYLOSER = 7 #when any friendly fighter loses
    ONDRAW = 8
    WHENCYCLED = 9
    POWERCHANGE = 10
    ONANYINITIALIZE = 11
    ONFRIENDLYPOWERCOUNTER = 12
    ONOPPONENTDRAW = 13
    GUNNERFIGHTS = 14
    ONFRIENDLYGUNNERPLAYED = 15
    NONE = 16
    
class EffectType(Enum):
    POWERCOUNTER = 1
    SCRAP = 2
    CYCLE = 3
    PLAYCARD = 4
    DESTROYCARD = 5
    SETFIGHTERDESTINATION = 6
    SETOPPOSINGFIGHTERDESTINATION = 7
    REPLACEFIGHTER = 8
    ALWAYSTIES = 9
    CANTHAVEPOWERCOUNTERS = 10
    
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
    CURRENTFIGHTER = 13
    RANDOMENEMYFIGHTER = 14
    ACTIVECARD = 15

class TargetFilter(Enum):
    NOFILTER = 1
    ATHYR = 2
    LEANOR = 3
    RANCE = 4
    HASPOWERCOUNTER = 5
    LOWESTPOWER = 6
    RANDOM = 7

class Condition(Enum):
    NONE = 1
    ACTIVECARDHASPOWER = 2
    TEAMHASATLEASTXGUNNERS = 3
    REPLACINGWINNER = 4
    SELFHASPOWER = 5
    ACTIVECARDISATHYR = 6
    ACTIVECARDISLEANOR = 7
    ACTIVECARDISRANCE = 8
    ENEMYHASFIGHTERWITHPOWER = 9
    OPPONENTHASMOREFIGHTERS = 10

class IntValue(Enum):
    CURRENTPOWERCOUNTERS = 1
    REMOVEALLPOWERCOUNTERS = 2
    DOUBLEPOWERCOUNTERS = 3
    CYCLEDCARD = 4
    POWEROFVICTOR = 5
    TEAMSLOT = 6
    
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
    "initializeOnePowerCounterLeftmost": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.LEFTMOST, 1),
    "initializeOnePowerCounterRightmost": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.RIGHTMOST, 1),
    "initializeOnePowerCounterAll": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1),
    "initializeCycleOne": Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.NONE, 1),
    "onDrawOnePowerCounterSelf": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, 1),
    "onDrawOnePowerCounterLeftmost": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.LEFTMOST, 1),
    "whenCycledPlayCard": Effect(Timing.WHENCYCLED, EffectType.PLAYCARD, Target.SELF, 1),
    "onDrawOnePowerCounterAllIfCardIsOnePower": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDHASPOWER, 1),
    "loserCycleThree": Effect(Timing.LOSER, EffectType.CYCLE, Target.NONE, 3),
    "initializeOnePowerCounterAllAthyr": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1).addTargetFilter(TargetFilter.ATHYR),
    "initializeRemoveOnePowerCounterLeftmost": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.LEFTMOST, -1).addTargetFilter(TargetFilter.HASPOWERCOUNTER),
    "bodySnatcherEffect": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, IntValue.CYCLEDCARD).addNumberTimesToFire(1),
    "anyWinnerCycleOne": Effect(Timing.ANYWINNER, EffectType.CYCLE, Target.NONE, 1),
    "anyLoserCycleOne": Effect(Timing.ANYLOSER, EffectType.CYCLE, Target.NONE, 1),
    "initializeBothCycleOne": Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.BOTHPLAYERS, 1),
    "onOpponentDrawPowerCounterLeftmost": Effect(Timing.ONOPPONENTDRAW, EffectType.POWERCOUNTER, Target.LEFTMOST, 1),
    "onOpponentDrawPowerCounterRightmost": Effect(Timing.ONOPPONENTDRAW, EffectType.POWERCOUNTER, Target.RIGHTMOST, 1),
    "initializeFourPowerCountersSelfIfFourFighters": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 4).addCondition(Condition.TEAMHASATLEASTXGUNNERS, 4),
    "initializeTwoPowerCountersRandomLeanor": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.RANDOM, 2).addTargetFilter(TargetFilter.LEANOR),
    "initializeReplaceWinnerTwoPowerCountersAll": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 2).addCondition(Condition.REPLACINGWINNER, 0),
    "initializePowerCountersEqualToTeamSlot": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, IntValue.TEAMSLOT),
    "destroyIfPowerOne": Effect(Timing.POWERCHANGE, EffectType.DESTROYCARD, Target.SELF, 0).addCondition(Condition.SELFHASPOWER, 1),
    "destroyIfPowerTen": Effect(Timing.POWERCHANGE, EffectType.DESTROYCARD, Target.SELF, 0).addCondition(Condition.SELFHASPOWER, 10),
    "onAnyInitializeOnePowerCounterSelf": Effect(Timing.ONANYINITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1),
    "sparkyTombManEffect": Effect(Timing.LOSER, EffectType.SETOPPOSINGFIGHTERDESTINATION, Target.DISCARD, 0),
    "loserPutBackInDeck": Effect(Timing.LOSER, EffectType.SETFIGHTERDESTINATION, Target.DECK, 0),
    "transferPowerCountersToReplacement": Effect(Timing.AFTERWINNING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, IntValue.CURRENTPOWERCOUNTERS),
    "powerCounterSelfOnTeammatePowerCounter": Effect(Timing.ONFRIENDLYPOWERCOUNTER, EffectType.POWERCOUNTER, Target.SELF, 1),
    "powerCounterAllLeanorWhenLeanorWins": Effect(Timing.ANYWINNER, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDISLEANOR, 1).addTargetFilter(TargetFilter.LEANOR),
    "powerCounterAllLeanorWhenLeanorLoses": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.ALL, 1).addCondition(Condition.ACTIVECARDISLEANOR, 1).addTargetFilter(TargetFilter.LEANOR),
    "winnerPowerCounterAll": Effect(Timing.WINNER, EffectType.POWERCOUNTER, Target.ALL, 1),
    "anyWinnerTwoPowerCountersSelf": Effect(Timing.ANYWINNER, EffectType.POWERCOUNTER, Target.SELF, 2),
    "anyLoserTwoPowerCountersSelf": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.SELF, 2),
    "anyLoserOnePowerCounterAll": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.ALL, 1),
    "anyLoserOnePowerCounterRandom": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.RANDOM, 1),
    "anyLoserOnePowerCounterLeftmost": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.LEFTMOST, 1),
    "anyLoserOnePowerCounterRightmost": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.RIGHTMOST, 1),
    "anyLoserTwoPowerCountersLeftmost": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.LEFTMOST, 2),
    "anyLoserTwoPowerCountersRightmost": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.RIGHTMOST, 2),
    "anyLoserThreePowerCountersSelf": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.SELF, 3),
    "anyLoserFourPowerCountersRandom": Effect(Timing.ANYLOSER, EffectType.POWERCOUNTER, Target.RANDOM, 4),
    "initializeTenPowerCountersIfOpponentHasTenPower": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 10).addCondition(Condition.ENEMYHASFIGHTERWITHPOWER, 10),
    "initializeOnePowerCounterAllFriendlyLeanor": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1).addTargetFilter(TargetFilter.LEANOR),
    "initializeRemoveAllPowerCounters": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, IntValue.REMOVEALLPOWERCOUNTERS),
    "loserReplace": Effect(Timing.LOSER, EffectType.REPLACEFIGHTER, Target.SELF, 0),
    "loserRemoveAllPowerCounters": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.ALL, IntValue.REMOVEALLPOWERCOUNTERS),
    "loserTwoPowerCountersLeftmost": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.LEFTMOST, 2),
    "loserTwoPowerCountersRightmost": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.RIGHTMOST, 2),
    "loserSixPowerCountersRightmost": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.RIGHTMOST, 6),
    "loserVictorPowerToRandom": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.RANDOM, IntValue.POWEROFVICTOR),
    "loserTwoPowerCountersAllRance": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.ALL, 2).addTargetFilter(TargetFilter.RANCE),
    "afterLosingOnePowerCounterReplacement": Effect(Timing.AFTERLOSING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, 1),
    "afterLosingTwoPowerCountersReplacement": Effect(Timing.AFTERLOSING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, 2),
    "afterWinningThreePowerCountersReplacement": Effect(Timing.AFTERWINNING, EffectType.POWERCOUNTER, Target.REPLACEMENTFIGHTER, 3),
    "loserDoublePowerCountersAll": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.ALL, IntValue.DOUBLEPOWERCOUNTERS),
    "hapthorEffect": Effect(Timing.ANYLOSER, EffectType.REPLACEFIGHTER, Target.CURRENTFIGHTER, 0),
    "hapthorEffectSelf": Effect(Timing.ANYLOSER, EffectType.REPLACEFIGHTER, Target.SELF, 0),
    "loserSixPowerCountersRandom": Effect(Timing.LOSER, EffectType.POWERCOUNTER, Target.RANDOM, 6),
    "loserKamakazeEffect": Effect(Timing.LOSER, EffectType.DESTROYCARD, Target.RANDOMENEMYFIGHTER, 0).addCondition(Condition.OPPONENTHASMOREFIGHTERS, 0),
    "alwaysTiesFight": Effect(Timing.NONE, EffectType.ALWAYSTIES, Target.SELF, 0),
    "cannotHavePowerCounters": Effect(Timing.NONE, EffectType.CANTHAVEPOWERCOUNTERS, Target.SELF, 0),
    "onFriendlyGunnerPlayedOnePowerCounterActiveCard": Effect(Timing.ONFRIENDLYGUNNERPLAYED, EffectType.POWERCOUNTER, Target.ACTIVECARD, 1),
    "loserScrapSelf": Effect(Timing.LOSER, EffectType.SCRAP, Target.SELF, 0),
    "winnerScrapSelf": Effect(Timing.WINNER, EffectType.SCRAP, Target.SELF, 0),
}