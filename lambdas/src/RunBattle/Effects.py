from enum import Enum

class Timing(Enum):
    INITIALIZE = 1
    WINNER = 2
    LOSER = 3
    SIGNINGBONUS = 4
    ONDRAW = 5
    
class EffectType(Enum):
    POWERCOUNTER = 1
    SCRAP = 2
    CYCLE = 3
    
class Target(Enum):
    SELF = 1
    LEFTMOST = 2
    RIGHTMOST = 3
    RANDOM = 4
    ALL = 5
    NONE = 6
    
class Effect:
    def __init__(self, timing, effectType, target, intValue):
        self.timing = timing
        self.effectType = effectType
        self.target = target
        self.intValue = intValue
        
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
    
effects = {
    "initializeOnePowerCounterSelf": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 1),
    "initializeTwoPowerCounterSelf": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 2),
    "initializeThreePowerCounterSelf": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.SELF, 3),
    "initializeOnePowerCounterAll": Effect(Timing.INITIALIZE, EffectType.POWERCOUNTER, Target.ALL, 1),
    "initializeCycleOne": Effect(Timing.INITIALIZE, EffectType.CYCLE, Target.NONE, 1),
    "onDrawOnePowerCounterSelf": Effect(Timing.ONDRAW, EffectType.POWERCOUNTER, Target.SELF, 1)
}