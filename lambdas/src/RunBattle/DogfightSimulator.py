from Player import Player
from Animations import Animations
from enum import Enum

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
                self.playerOne.gunnerWins()
                self.playerTwo.gunnerLoses()
                self.playerOne.activateGunnerWinsEffects()
                self.playerTwo.activateGunnerLosesEffects()
            elif fighterTwoPower > fighterOnePower:
                #fighterTwo wins
                self.playerOne.gunnerLoses()
                self.playerTwo.gunnerWins()
                self.playerOne.activateGunnerLosesEffects()
                self.playerTwo.activateGunnerWinsEffects()
                #write the animation code
            else:
                #fighters tie
                self.playerOne.gunnerLoses()
                self.playerTwo.gunnerLoses()
                self.playerOne.activateGunnerLosesEffects()
                self.playerTwo.activateGunnerLosesEffects()
            self.animations.append('b,gd,' + self.playerOne.getFighterDestination() + ',' + self.playerTwo.getFighterDestination())
            #self.playerOne.printTeam()
            #self.playerOne.printDiscard()
            #self.playerTwo.printTeam()
            #self.playerTwo.printDiscard()
        #end while
        if self.playerOne.stillAlive():
            self.animations.append('p,1w,0,0')
        elif self.playerTwo.stillAlive():
            self.animations.append('s,2w,0,0')
        else:
            self.animations.append('b,ft,0,0')