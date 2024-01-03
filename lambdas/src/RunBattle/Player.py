import random
from Cards import Card
from Effects import Timing
from Effects import Target
from Effects import TargetFilter
from enum import IntEnum
from copy import deepcopy

class FighterDestination(IntEnum):
    DECK = 0
    DISCARD = 1

class Player:
    def __init__(self, deckString, playerIdentifier, animations):
        deckStringList = deckString.split(',')
        self.deck = []
        for cardIdString in deckStringList:
            thisCard = Card.withId(int(cardIdString), animations)
            self.deck.append(thisCard)
        self.team = [None, None, None, None, None, None]
        self.discard = []
        self.activeCard = None
        self.playerIdentifier = playerIdentifier
        self.currentRoll = 0
        self.opponent = None
        self.animations = animations
        self.fighterDestination = FighterDestination.DECK

    def addOpponent(self, opponent):
        self.opponent = opponent
        
    def shuffleDeck(self):
        random.shuffle(self.deck)
        return self.deck
        
    def rollDie(self):
        self.currentRoll = random.randint(1, 6)
        for card in self.team:
            if (card != None):
                card.isReplacement = False
        return self.currentRoll
        
    def drawCard(self):
        if (len(self.deck) > 0):
            self.animations.append(self.playerIdentifier + ",dws,1,0")
            self.activeCard = self.deck.pop(0)
            #activate draw card effects of cards on team
            self.activateEffectsForTeam(Timing.ONDRAW)
            self.activateEffectsForOpponentTeam(Timing.ONOPPONENTDRAW)
        else:
            self.animations.append(self.playerIdentifier + ",ded,0,0")
            self.activeCard = None

    def activateEffectsForTeam(self, timing):
        for card in self.team:
            if (card != None):
                card.activateEffectsFor(timing, self)

    def activateEffectsForTeammates(self, timing, teamSlotToAvoid):
        for card in self.team:
            if (card != None and card.teamSlot != teamSlotToAvoid):
                card.activateEffectsFor(timing, self)

    def activateEffectsForOpponentTeam(self, timing):
        if self.opponent != None:
            for card in self.opponent.team:
                if (card != None):
                    card.activateEffectsFor(timing, self.opponent)
            
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
        
    def drawAndPlayCard(self, slotToPlayCardIn):
        if (self.team[slotToPlayCardIn - 1] == None):
            self.drawCard()
            self.playCard(slotToPlayCardIn)

    def replaceWinner(self, slotToPlayCardIn):
        if (self.team[slotToPlayCardIn - 1] == None):
            self.drawCard()
            self.activeCard.replacingWinner = True
            self.playCard(slotToPlayCardIn)

    def drawCardSetupStep(self):
        if (self.leftmostOpenTeamSlot() > 0):
            #means there is an open gunner slot
            self.drawCard()
            self.playCard(self.leftmostOpenTeamSlot())

    def openingDrawShouldOccur(self):
        if (len(self.deck) == 0):
            return False
        if self.leftmostOpenTeamSlot() > 0:
            return True
        return False
        
    def cycleCard(self):
        if (len(self.deck) > 0):
            self.drawCard()
            #self.activeCard is the drawn card
            self.activeCard.activateEffectsFor(Timing.WHENCYCLED, self)
            if (self.activeCard != None):
                #means self.activeCard was not played
                self.animations.append(self.playerIdentifier + ",uns,1,0")
                self.putCardOnBottomOfDeck()
        
    
    def gunnerFromRoll(self):
        return self.team[self.gunnerIndexFromRoll()]
    
    def gunnerIndexFromRoll(self):
        return self.gunnerIndexFromSlot(self.currentRoll)
            
    def gunnerIndexFromSlot(self, slotNumber):
        for index in range(0,6):
            thisIndex = slotNumber - 1 + index
            if thisIndex >= 6:
                thisIndex = thisIndex - 6
            if self.team[thisIndex] != None:
                return thisIndex
            
    def gunnerIndexFromSlotWithFilter(self, slotNumber, effect):
        for index in range(0,6):
            thisIndex = slotNumber - 1 + index
            if thisIndex >= 6:
                thisIndex = thisIndex - 6
            if self.team[thisIndex] != None and self.team[thisIndex].passesFilter(effect):
                return thisIndex
        return None
            
    def leftmostOpenTeamSlot(self):
        for index in range(0,6):
            if (self.team[index] == None):
                return index + 1
        return 0
        
    def gunnerWins(self):
        self.currentFighter = self.gunnerFromRoll()
        self.team[self.currentFighter.teamSlot - 1] = None
        self.fighterDestination = FighterDestination.DECK

    def activateGunnerWinsEffects(self):
        self.activateEffectsForTeam(Timing.ANYWINNER)
        self.currentFighter.activateEffectsFor(Timing.WINNER, self)
        if len(self.deck) > 0 and self.team[self.currentFighter.teamSlot - 1] == None: #if card was in deck before gunner was put back in deck and the slot is still available
            self.replaceWinner(self.currentFighter.teamSlot)
        self.currentFighter.activateEffectsFor(Timing.AFTERWINNING, self)
        self.sendFighterToDestination(self.currentFighter)
            
    def gunnerLoses(self):
        self.currentFighter = self.gunnerFromRoll()
        self.team[self.currentFighter.teamSlot - 1] = None
        self.fighterDestination = FighterDestination.DISCARD
    
    def activateGunnerLosesEffects(self):
        self.activateEffectsForTeam(Timing.ANYLOSER)
        self.currentFighter.activateEffectsFor(Timing.LOSER, self)
        self.currentFighter.activateEffectsFor(Timing.AFTERLOSING, self)
        self.sendFighterToDestination(self.currentFighter)

    def clearCurrentFighter(self):
        self.currentFighter.clear()
        self.currentFighter = None

    def setFighterDestination(self, effect):
        match effect.target:
            case Target.DECK:
                self.fighterDestination = FighterDestination.DECK
            case Target.DISCARD:
                self.fighterDestination = FighterDestination.DISCARD

    def sendFighterToDestination(self, fighterToSend):
        if (self.fighterDestination == FighterDestination.DECK):
            self.deck.append(fighterToSend)
        elif (self.fighterDestination == FighterDestination.DISCARD):
            self.discard.append(fighterToSend)
    
    def destroyCardFromEffect(self, cardToDestroy, effect):
        self.team[cardToDestroy.teamSlot - 1] = None
        self.discard.append(cardToDestroy)
        self.animations.append(self.playerIdentifier + ",des,0," + str(cardToDestroy.teamSlot))
        if (effect.target == Target.SELF):
            self.fighterDestination = FighterDestination.DISCARD
        cardToDestroy.clear()

    def hasFighterWithPower(self, powerToMatch):
        for card in self.team:
            if (card != None) and (card.getTotalPower() >= powerToMatch):
                return True
        return False

    def replaceFighterEffect(self, cardToReplace):
        if (self.team[cardToReplace.teamSlot - 1] == None): #no card there yet
            self.drawCard()
            if self.activeCard != None:
                self.activeCard.isReplacement = True
                self.playCard(cardToReplace.teamSlot)
        else: #card is already there
            cardInSlot = self.team[cardToReplace.teamSlot - 1]
            if (not cardInSlot.isReplacement and len(self.deck) > 0):
                self.sendInactiveFighterToBottomOfDeck(cardToReplace)
                self.drawCard()
                self.activeCard.isReplacement = True
                self.playCard(cardToReplace.teamSlot)
        
                
    def sendInactiveFighterToBottomOfDeck(self, cardToReplace):
        self.deck.append(self.team[cardToReplace.teamSlot - 1])
        self.team[cardToReplace.teamSlot - 1] = None
        self.animations.append(self.playerIdentifier + ",fbd," + str(cardToReplace.teamSlot) + ",0")
            
    def getFighterDestination(self):
        return str(int(self.fighterDestination))
        
    def stillAlive(self):
        for fighter in self.team:
            if fighter != None:
                return True
        return False
    
    def numberFightersRemaining(self):
        fightersRemaining = 0
        for fighter in self.team:
            if fighter != None:
                fightersRemaining += 1
        return fightersRemaining
    
    def pointsScored(self):
        points = 0
        for fighter in self.team:
            if fighter != None:
                points += 1
        return points
        
    def printTeam(self):
        print("--- " + self.playerIdentifier + " team ---")
        teamString = ""
        for card in self.team:
            if card == None:
                teamString += " (None) "
            else:
                teamString += " (" + card.name + ": " + str(card.power + card.powerCounters) + ") "
        print(teamString)
    
    def printDiscard(self):
        print("---------= " + self.playerIdentifier + " discard =---------")
        discardString = ""
        for card in self.discard:
            if card == None:
                discardString += " (None) "
            else:
                discardString += " (" + card.name + ": " + str(card.power + card.powerCounters) + ") "
        print(discardString)