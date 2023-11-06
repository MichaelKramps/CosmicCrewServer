using UnityEngine;
using System.Collections.Generic;

public class DiscardPile
{
    List<GameObject> discardPile;

    public DiscardPile()
    {
        discardPile = new List<GameObject>();
    }

    public void discard(GameObject cardToBeDiscarded)
    {
        discardPile.Add(cardToBeDiscarded);
    }
}
