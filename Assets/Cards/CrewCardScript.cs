using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class CrewCardScript : MonoBehaviour
{
    public CrewCard crewCard;

    public TMPro.TextMeshPro cardName;
    public TMPro.TextMeshPro customText;
    public TMPro.TextMeshPro power;
    public TMPro.TextMeshPro civilizationType;
    public SpriteRenderer cardArt;

    // Start is called before the first frame update
    void Start()
    {
        cardName.text = crewCard.cardName;
        customText.text = crewCard.cardText;
        power.text = crewCard.power.ToString();
        cardArt.sprite = crewCard.cardArt;

        switch(crewCard.civilizationType)
        {
            case CivilizationType.Athyr:
                civilizationType.text = "Athyr";
                break;
            case CivilizationType.Leanor:
                civilizationType.text = "Leanor";
                break;
            case CivilizationType.Rance:
                civilizationType.text = "Rance";
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
