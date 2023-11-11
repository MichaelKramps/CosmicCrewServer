from Effects import EffectType

class Animations:
    animationsList = []

    @staticmethod
    def append(animationCode):
        Animations.animationsList.append(animationCode)

    @staticmethod
    def addCodeFrom(player, effect, intValue, secondIntValue):
        Animations.animationsList.append(Animations.animationCodeFrom(player, effect, intValue, secondIntValue))

    @staticmethod
    def animationCodeFrom(player, effect, intValue, secondIntValue):
        animationCode = player.playerIdentifier + "," 
        animationCode += Animations.effectToCode(effect) + ","
        animationCode += str(intValue) + ","
        animationCode += str(secondIntValue)
        return animationCode

    @staticmethod
    def effectToCode(effect):
        match effect.effectType:
            case EffectType.POWERCOUNTER:
                return "pow"
            case EffectType.SCRAP:
                return "scr"
            
    @staticmethod
    def codesAppearInOrder(codes):
        for existingCodeIndex in range(len(Animations.animationsList)):
            matchedAllCodes = True
            for searchingCodeIndex in range(len(codes)):
                if Animations.animationsList[existingCodeIndex + searchingCodeIndex] != codes[searchingCodeIndex]:
                    matchedAllCodes = False
                    break
            if matchedAllCodes:
                return matchedAllCodes
        return False

            
    @staticmethod
    def clearAnimations():
        Animations.animationsList = []

    