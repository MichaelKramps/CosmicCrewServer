from enum import Enum

class Timing(Enum):
    INITIALIZE = 1
    WINNER = 2
    LOSER = 3
    SIGNINGBONUS = 4
    ONDRAW = 5
    WHENCYCLED = 6
    
class EffectType(Enum):
    POWERCOUNTER = 1
    SCRAP = 2
    CYCLE = 3
    PLAYCARD = 4
    
class Target(Enum):
    SELF = 1
    LEFTMOST = 2
    RIGHTMOST = 3
    RANDOM = 4
    ALL = 5
    NONE = 6

class TargetFilter(Enum):
    NOFILTER = 1
    ATHYR = 2
    LEANOR = 3
    RANCE = 4

class Condition(Enum):
    NONE = 1
    ACTIVECARDHASPOWER = 2
    
class Effect:
    def __init__(self, timing, effectType, target, intValue):
        self.timing = timing
        self.effectType = effectType
        self.target = target
        self.condition = Condition.NONE
        self.intValue = intValue
        self.conditionValue = 0
        self.targetFilter = TargetFilter.NOFILTER
        
    def getAnimationCode(self, player, card):
        #player,effectCode,target,intValue
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
            case EffectType.CYCLE:
                return "cyc,"
            
    def addCondition(self, condition, conditionValue):
        self.condition = condition
        self.conditionValue = conditionValue
        return self
    
    def addTargetFilter(self, filter):
        self.targetFilter = filter
        return self
    
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
    "initializeOnePowerCounterAllAthyr": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1).addTargetFilter(TargetFilter.ATHYR)
}