import random
from Cards import Card
from Effects import Timing
from copy import deepcopy

class Player:
    def __init__(self, deckString, playerIdentifier, animations):
        deckStringList = deckString.split(',')
        self.deck = []
        for cardIdString in deckStringList:
            thisCard = Card.getCardWithId(int(cardIdString), animations)
            self.deck.append(thisCard)
        self.team = [None, None, None, None, None, None]
        self.discard = []
        self.activeCard = None
        self.playerIdentifier = playerIdentifier
        self.currentRoll = 0
        self.animations = animations
        
    def shuffleDeck(self):
        random.shuffle(self.deck)
        return self.deck
        
    def rollDie(self):
        self.currentRoll = random.randint(1, 6)
        return self.currentRoll
        
    def drawCard(self):
        if (len(self.deck) > 0):
            self.animations.append(self.playerIdentifier + ",dws,1,0")
            self.activeCard = self.deck.pop(0)
            #activate draw card effects of cards on team
            for card in self.team:
                if (card != None):
                    card.activateEffectsFor(Timing.ONDRAW, self)
        else:
            self.animations.append(self.playerIdentifier + ",ded,0,0")
            self.activeCard = None
            
    def putCardOnBottomOfDeck(self):
        if (self.activeCard != None):
            self.activeCard.clear()
            self.deck.append(self.activeCard)
            self.activeCard = None
        else:
            self.animations.append(self.playerIdentifier + ",ded,0,0")
        
    def playCard(self, slotToPlayCardIn):
        if (self.activeCard != None):
            self.team[slotToPlayCardIn - 1] = self.activeCard
            self.activeCard.teamSlot = slotToPlayCardIn
            self.animations.append(self.playerIdentifier + ",p," + str(slotToPlayCardIn) + ",0")
            self.activeCard.activateEffectsFor(Timing.INITIALIZE, self)
            self.activeCard = None
            self.printTeam()
        
    def drawAndPlayCard(self, slotToPlayCardIn):
        self.drawCard()
        self.playCard(slotToPlayCardIn)

    def drawCardSetupStep(self):
        if (self.leftmostOpenTeamSlot() > 0):
            #means there is an open gunner slot
            self.drawCard()
            self.playCard(self.leftmostOpenTeamSlot())
        
    def cycleCard(self):
        if (len(self.deck) > 0):
            self.drawCard()
            #self.activeCard is the drawn card
            self.activeCard.activateEffectsFor(Timing.WHENCYCLED, self)
            if (self.activeCard != None):
                #means self.activeCard was not played
                self.animations.append(self.playerIdentifier + ",uns,1,0");
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
            
    def leftmostOpenTeamSlot(self):
        for index in range(0,6):
            if (self.team[index] == None):
                return index + 1
        return 0
        
    def gunnerWins(self):
        self.activeCard = self.gunnerFromRoll()
        self.activeCard.clear()
        deckWasNotEmpty = len(self.deck) > 0
        self.deck.append(self.activeCard)
        indexOfWinningGunner = self.gunnerIndexFromRoll()
        self.team[indexOfWinningGunner] = None
        self.activeCard.activateEffectsFor(Timing.WINNER, self)
        if deckWasNotEmpty:
            self.drawAndPlayCard(indexOfWinningGunner + 1)
            
    def gunnerLoses(self):
        self.activeCard = self.gunnerFromRoll()
        self.activeCard.clear()
        self.discard.append(self.activeCard)
        self.team[self.gunnerIndexFromRoll()] = None
        self.activeCard.activateEffectsFor(Timing.LOSER, self)
        self.activeCard = None

        
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