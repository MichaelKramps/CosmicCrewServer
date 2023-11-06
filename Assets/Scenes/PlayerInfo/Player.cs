using System;
using UnityEngine;

public class Player
{
    private CrewDeck crewDeck;
    private BattlefieldTeam battlefieldTeam;
    private DiscardPile discardPile;

    public Player()
    {
        crewDeck = new CrewDeck();
        battlefieldTeam = new BattlefieldTeam();
        discardPile = new DiscardPile();
    }

    public void addCardToDeck(GameObject crewCard)
    {
        crewDeck.addCard(crewCard);
    }

    public GameObject drawCard()
    {
        return crewDeck.drawCard();
    }

    public void playCard(GameObject cardToPlay)
    {
        battlefieldTeam.playCard(cardToPlay);
    }

    public GameObject gunnerFromRoll(int gunnerSlotNumber)
    {
        return battlefieldTeam.gunnerFromRoll(gunnerSlotNumber);
    }

    public void discardGunner(int numberRolled)
    {
        discardPile.discard(battlefieldTeam.gunnerFromRoll(numberRolled));
        battlefieldTeam.removeGunnerFromRoll(numberRolled);
    }

    public void putGunnerAtBottomOfDeck(int battlefieldTeamIndexOfDiscardedGunner)
    {
        crewDeck.addCard(battlefieldTeam.gunnerFromRoll(battlefieldTeamIndexOfDiscardedGunner));
        battlefieldTeam.removeGunnerFromRoll(battlefieldTeamIndexOfDiscardedGunner);
    }

    public int indexOfFirstAvailableGunner(int rolledNumber)
    {
        return battlefieldTeam.indexOfFirstAvailableGunner(rolledNumber);
    }
}
