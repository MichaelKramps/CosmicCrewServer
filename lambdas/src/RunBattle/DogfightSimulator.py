from Player import Player
from Animations import Animations

class DogfightSimulator:
    def __init__(self, deckOne, deckTwo):
        self.playerOne = Player(deckOne, "p")
        self.playerTwo = Player(deckTwo, "s")
    
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
        cardSlot = 1;
        while (len(self.playerOne.deck) > 0 and len(self.playerTwo.deck) > 0 and cardSlot <=6):
            self.playerOne.drawAndPlayCard(cardSlot)
            self.playerTwo.drawAndPlayCard(cardSlot)
            cardSlot += 1
            
        if (len(self.playerOne.deck) > 0 and cardSlot <=6):
            while (len(self.playerOne.deck) > 0 and cardSlot <= 6):
                self.playerOne.drawAndPlayCard(cardSlot)
                cardSlot += 1
        elif (len(self.playerTwo.deck) > 0 and cardSlot <=6):
            while (len(self.playerTwo.deck) > 0 and cardSlot <= 6):
                self.playerTwo.drawAndPlayCard(cardSlot)
                cardSlot += 1
                    
    def fight(self):
        while(self.playerOne.stillAlive() and self.playerTwo.stillAlive()):
            rollOne = self.playerOne.rollDie()
            rollTwo = self.playerTwo.rollDie()
            Animations.animationsList.append('b,r,' + str(rollOne) + ',' + str(rollTwo))
            fighterOne = self.playerOne.gunnerFromRoll()
            fighterTwo = self.playerTwo.gunnerFromRoll()
            fighterOnePower = fighterOne.power + fighterOne.powerCounters
            fighterTwoPower = fighterTwo.power + fighterTwo.powerCounters
            if fighterOnePower > fighterTwoPower:
                #fighterOne wins
                Animations.animationsList.append('b,g1,' + str(rollOne) + ',' + str(rollTwo))
                replaceGunner = self.playerOne.gunnerWins()
                self.playerTwo.gunnerLoses()
            elif fighterTwoPower > fighterOnePower:
                #fighterTwo wins
                Animations.animationsList.append('b,g2,' + str(rollOne) + ',' + str(rollTwo))
                self.playerOne.gunnerLoses()
                replaceGunner = self.playerTwo.gunnerWins()
                #write the animation code
            else:
                #fighters tie
                self.playerOne.gunnerLoses()
                self.playerTwo.gunnerLoses()
                #write the animation code
                Animations.animationsList.append('b,gt,' + str(rollOne) + ',' + str(rollTwo))
        #end while
        if self.playerOne.stillAlive():
            Animations.animationsList.append('p,1w,0,0')
        elif self.playerTwo.stillAlive():
            Animations.animationsList.append('s,2w,0,0')
        else:
            Animations.animationsList.append('b,ft,0,0')