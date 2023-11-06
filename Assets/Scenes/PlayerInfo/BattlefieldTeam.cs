using System.Collections.Generic;
using UnityEngine;

public class BattlefieldTeam
{
    public List<GameObject> gunners;
    public int indexToAnimateTo;

    public BattlefieldTeam()
    {
        gunners = new List<GameObject> { null, null, null, null, null, null };
    }

    public void playCard(GameObject cardToPlay)
    {
        //returns the index of gunner slot with the lowest index
        int indexToPlay = getLowestOpenIndex();
        
        if (indexToPlay >= 0)
        {
            gunners[indexToPlay] = cardToPlay;
        }

        indexToAnimateTo = indexToPlay;
    }

    private int getLowestOpenIndex() {
        //returns -1 if no openings
        for (int index = 0; index < gunners.Count; index++)
        {
            if (gunners[index] == null)
            {
                return index;
            }
        }
        return -1;
    }

    public GameObject gunnerFromRoll(int numberRolled)
    {
        return gunners[indexOfFirstAvailableGunner(numberRolled)];
    }

    public void removeGunnerFromRoll(int numberRolled)
    {
        gunners[indexOfFirstAvailableGunner(numberRolled)] = null;
    }

    public int indexOfFirstAvailableGunner(int numberRolled)
    {
        if (gunners[numberRolled - 1] != null)
        {
            return numberRolled - 1;
        } else
        {
            if (numberRolled == 6)
            {
                return indexOfFirstAvailableGunner(1);
            } else
            {
                return indexOfFirstAvailableGunner(numberRolled + 1);
            }
        }
    }
}
