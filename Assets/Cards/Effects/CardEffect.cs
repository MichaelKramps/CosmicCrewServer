using UnityEngine;
using System.Collections;

[CreateAssetMenu(fileName = "New Card Effect", menuName = "CardEffect")]
public class CardEffect : ScriptableObject
{
    public CardEffectTiming cardTiming;
    public CardEffectType typeOfEffect;
    public CardEffectTarget effectTarget;
    public CardEffectCondition effectCondition;
    public int effectAmplitudeA;
    public int effectAmplitudeB;
    public int contidionAmplitudeA;
    public int contidionAmplitudeb;
}
