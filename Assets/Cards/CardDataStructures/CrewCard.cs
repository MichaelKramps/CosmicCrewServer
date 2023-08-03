using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[CreateAssetMenu(fileName = "CrewCard", menuName = "Cards/CrewCard")]
public class CrewCard : ScriptableObject
{
    public CrewCardType crewCardType;
    public string cardName;
    public string cardText;

    public Sprite image;

    public int powerCost;
    public int baseOffense;
    public int currentOffense;
    public int baseDefense;
    public int currentDefense;
    public GunnerSlot gunnerSlot;
    public CivilizationType civilizationType;

    public List<CardEffect> cardEffects;
}