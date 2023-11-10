import random
from Cards import cardList
from Animations import Animations
from Effects import Timing
from copy import deepcopy

class Player:
    def __init__(self, deckString, playerIdentifier):
        deckStringList = deckString.split(',')
        self.deck = []
        for cardIdString in deckStringList:
            thisCard = deepcopy(cardList[int(cardIdString)])
            self.deck.append(thisCard)
        self.team = [None, None, None, None, None, None]
        self.discard = []
        self.activeCard = None
        self.playerIdentifier = playerIdentifier
        self.currentRoll = 0
        
    def shuffleDeck(self):
        random.shuffle(self.deck)
        return self.deck
        
    def rollDie(self):
        self.currentRoll = random.randint(1, 6)
        return self.currentRoll
        
    def drawCard(self):
        Animations.animationsList.append(self.playerIdentifier + ",dws,1,0")
        if (len(self.deck) > 0):
            self.activeCard = self.deck.pop(0)
            #activate draw card effects of cards on team
            for card in self.team:
                if (card != None):
                    card.activateEffectsFor(Timing.ONDRAW, self)
        else:
            self.activeCard = None
            
    def putCardOnBottomOfDeck(self):
        self.activeCard.clear()
        self.deck.append(self.activeCard)
        self.activeCard = None
        
    def playCard(self, slotToPlayCardIn):
        self.team[slotToPlayCardIn - 1] = self.activeCard
        self.activeCard.teamSlot = slotToPlayCardIn
        Animations.animationsList.append(self.playerIdentifier + ",p," + str(slotToPlayCardIn) + ",0")
        self.activeCard.activateEffectsFor(Timing.INITIALIZE, self)
        self.activeCard = None
        self.printTeam()
        
    def drawAndPlayCard(self, slotToPlayCardIn):
        self.drawCard()
        return self.playCard(slotToPlayCardIn)
        
    def cycleCard(self):
        self.drawCard()
        Animations.animationsList.append(self.playerIdentifier + ",uns,1,0");
        self.putCardOnBottomOfDeck()
        
    
    def gunnerFromRoll(self):
        return self.team[self.gunnerIndexFromRoll()]
    
    def gunnerIndexFromRoll(self):
        for index in range(0,6):
            thisIndex = self.currentRoll - 1 + index
            if thisIndex >= 6:
                thisIndex = thisIndex - 6
            if self.team[thisIndex] != None:
                return thisIndex
        
    def gunnerWins(self):
        #check this before putting the winning gunner in the deck
        self.gunnerFromRoll().clear()
        deckWasNotEmpty = len(self.deck) > 0
        self.deck.append(self.gunnerFromRoll())
        indexOfWinningGunner = self.gunnerIndexFromRoll()
        self.team[indexOfWinningGunner] = None
        if deckWasNotEmpty:
            self.drawAndPlayCard(indexOfWinningGunner + 1)
            
    def gunnerLoses(self):
        self.gunnerFromRoll().clear()
        self.discard.append(self.gunnerFromRoll())
        self.team[self.gunnerIndexFromRoll()] = None
        
    def stillAlive(self):
        for fighter in self.team:
            if fighter != None:
                return True
        return False
        
    def printTeam(self):
        print("--- " + self.playerIdentifier + " team ---")
        teamString = ""
        for card in self.team:
            if card == None:
                teamString += " (None) "
            else:
                teamString += " (" + card.name + ": " + str(card.power + card.powerCounters) + ") "
        print(teamString)