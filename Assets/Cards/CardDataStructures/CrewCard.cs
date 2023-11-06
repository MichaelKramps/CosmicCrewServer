using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

[CreateAssetMenu(fileName = "CrewCard", menuName = "Cards/CrewCard")]
public class CrewCard : ScriptableObject
{
    public string cardName;
    public string cardText;

    public Sprite cardArt;

    public int power;
    public int powerCounters;
    public int cardId;
    public CivilizationType civilizationType;

    public List<CardEffect> cardEffects;
}