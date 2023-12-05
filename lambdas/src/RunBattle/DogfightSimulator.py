from Player import Player
from Animations import Animations

class DogfightSimulator:
    def __init__(self, deckOne, deckTwo, animations):
        self.animations = animations
        self.playerOne = Player(deckOne, "p", self.animations)
        self.playerTwo = Player(deckTwo, "s", self.animations)
        self.playerOne.addOpponent(self.playerTwo)
        self.playerTwo.addOpponent(self.playerOne)
    
    def simulateDogfight(self):
        self.playerOne.shuffleDeck()
        self.playerTwo.shuffleDeck()
        self.startingDeckOne = self.getStartingDeckString(self.playerOne.deck)
        self.startingDeckTwo = self.getStartingDeckString(self.playerTwo.deck)
        self.setupDogfight()
        self.fight()
        
    def getStartingDeckString(self, deck):
        deckString = ''
        for card in deck:
            deckString += str(card.id)
            deckString += ','
        return deckString[:-1]
        
    def setupDogfight(self):
        while self.playerOne.openingDrawShouldOccur() or self.playerTwo.openingDrawShouldOccur():
            self.playerOne.drawCardSetupStep()
            self.playerTwo.drawCardSetupStep()
                    
    def fight(self):
        while(self.playerOne.stillAlive() and self.playerTwo.stillAlive()):
            rollOne = self.playerOne.rollDie()
            rollTwo = self.playerTwo.rollDie()
            self.animations.append('b,r,' + str(rollOne) + ',' + str(rollTwo))
            fighterOne = self.playerOne.gunnerFromRoll()
            fighterTwo = self.playerTwo.gunnerFromRoll()
            fighterOnePower = fighterOne.power + fighterOne.powerCounters
            fighterTwoPower = fighterTwo.power + fighterTwo.powerCounters
            if fighterOnePower > fighterTwoPower:
                #fighterOne wins
                self.animations.append('b,g1,' + str(rollOne) + ',' + str(rollTwo))
                winningGunner = self.playerOne.gunnerWins()
                losingGunner = self.playerTwo.gunnerLoses()
                self.playerOne.activateGunnerWinsEffects(winningGunner)
                self.playerTwo.activateGunnerLosesEffects(losingGunner)
            elif fighterTwoPower > fighterOnePower:
                #fighterTwo wins
                self.animations.append('b,g2,' + str(rollOne) + ',' + str(rollTwo))
                losingGunner = self.playerOne.gunnerLoses()
                winningGunner = self.playerTwo.gunnerWins()
                self.playerOne.activateGunnerLosesEffects(losingGunner)
                self.playerTwo.activateGunnerWinsEffects(winningGunner)
                #write the animation code
            else:
                #fighters tie
                self.animations.append('b,gt,' + str(rollOne) + ',' + str(rollTwo))
                losingGunner1 = self.playerOne.gunnerLoses()
                losingGunner2 = self.playerTwo.gunnerLoses()
                self.playerOne.activateGunnerLosesEffects(losingGunner1)
                self.playerTwo.activateGunnerLosesEffects(losingGunner2)
        #end while
        if self.playerOne.stillAlive():
            self.animations.append('p,1w,0,0')
        elif self.playerTwo.stillAlive():
            self.animations.append('s,2w,0,0')
        else:
            self.animations.append('b,ft,0,0')