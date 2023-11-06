using System.Collections.Generic;
using UnityEngine;

public class CrewDeck
{
    private List<GameObject> deck;

    public CrewDeck()
    {
        deck = new List<GameObject> { };
    }

    public GameObject drawCard()
    {
        if (deck.Count > 0)
        {
            GameObject cardDrawn = deck[0];
            deck.Remove(cardDrawn);
            return cardDrawn;
        }

        return null;
    }

    public void addCard(GameObject cardToAdd)
    {
        deck.Add(cardToAdd);
    }
}
