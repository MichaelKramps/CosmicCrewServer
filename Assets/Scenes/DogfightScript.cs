using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DogfightScript : MonoBehaviour
{
    public GameObject crewCardPrefab;

    public List<CrewCard> deck1;
    public List<CrewCard> deck2;

    public int drawCounter1;
    public int drawCounter2;

    private DogfightStage currentStage = DogfightStage.Preparation;


    // Start is called before the first frame update
    void Start()
    {

        HandleDogfightStageChange();

    }

    void HandleDogfightStageChange()
    {
        switch(currentStage)
        {
            case DogfightStage.Preparation:
                // do any pre-fight animations and stuff
                currentStage = DogfightStage.Draw;
                HandleDogfightStageChange();
                break;
            case DogfightStage.Draw:
                DrawCards();
                break;
            default:
                Debug.Log("this stage is not handled yet!");
                break;
        }
    }

    void DrawCards()
    {
        // draw and show deck 1 card
        crewCardPrefab.GetComponent<CrewCardScript>().crewCard = deck1[0];
        GameObject card1 = Instantiate(
            crewCardPrefab,
            new Vector3(transform.position.x, transform.position.y - 2.5f, transform.position.z),
            transform.rotation);

        crewCardPrefab.GetComponent<CrewCardScript>().crewCard = deck2[0];
        GameObject card2 = Instantiate(
            crewCardPrefab,
            new Vector3(transform.position.x, transform.position.y + 2.5f, transform.position.z),
            transform.rotation);

        //make the cards get bigger
        // check out Animator
        card1.transform.localScale = new Vector3(1.5f, 1.5f);
        card2.transform.localScale = new Vector3(1.5f, 1.5f);
    }
}
