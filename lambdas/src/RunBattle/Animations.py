from Effects import EffectType

class Animations:
    def __init__(self):
        self.animationsList = []

    def append(self, animationCode):
        self.animationsList.append(animationCode)

    def addCodeFrom(self, player, effect, intValue, secondIntValue):
        self.animationsList.append(self.animationCodeFrom(player, effect, intValue, secondIntValue))

    def animationCodeFrom(self, player, effect, intValue, secondIntValue):
        animationCode = player.playerIdentifier + "," 
        animationCode += self.effectToCode(effect) + ","
        animationCode += str(intValue) + ","
        animationCode += str(secondIntValue)
        return animationCode

    def effectToCode(self, effect):
        match effect.effectType:
            case EffectType.POWERCOUNTER:
                return "pow"
            case EffectType.SCRAP:
                return "scr"
            
    def codesAppearInOrder(self, codes):
        for existingCodeIndex in range(len(self.animationsList)):
            matchedAllCodes = True
            for searchingCodeIndex in range(len(codes)):
                if self.animationsList[existingCodeIndex + searchingCodeIndex] != codes[searchingCodeIndex]:
                    matchedAllCodes = False
                    break
            if matchedAllCodes:
                return matchedAllCodes
        return False

    