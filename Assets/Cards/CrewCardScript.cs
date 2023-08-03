using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class CrewCardScript : MonoBehaviour
{
    public CrewCard crewCard;

    public SpriteRenderer gunnerSlot;

    public TMPro.TextMeshPro cardName;
    public TMPro.TextMeshPro customText;
    public TMPro.TextMeshPro powerCost;

    public TMPro.TextMeshPro offense;
    public TMPro.TextMeshPro defense;
    public TMPro.TextMeshPro civilizationType;

    // Start is called before the first frame update
    void Start()
    {
        cardName.text = crewCard.cardName;
        customText.text = crewCard.cardText;
        powerCost.text = crewCard.powerCost.ToString();

        if (crewCard.crewCardType == CrewCardType.Gunner)
        {
            Debug.Log("gunner here");
            offense.text = crewCard.baseOffense.ToString();
            defense.text = crewCard.baseDefense.ToString();

            switch(crewCard.gunnerSlot)
            {
                case GunnerSlot.Triangle:
                    Debug.Log("triangle here");
                    gunnerSlot.sprite = Resources.Load<Sprite>("black-triangle");
                    break;
                case GunnerSlot.Square:
                    gunnerSlot.sprite = Resources.Load<Sprite>("black-square");
                    break;
                case GunnerSlot.Circle:
                    gunnerSlot.sprite = Resources.Load<Sprite>("black-circle");
                    break;
                default:
                    break;
            }
        }

        switch(crewCard.civilizationType)
        {
            case CivilizationType.Athyr:
                civilizationType.text += "Athyr";
                break;
            case CivilizationType.Leanor:
                civilizationType.text += "Leanor";
                break;
            case CivilizationType.Rance:
                civilizationType.text += "Rance";
                break;
            default:
                // no type
                civilizationType.text = "";
                break;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
