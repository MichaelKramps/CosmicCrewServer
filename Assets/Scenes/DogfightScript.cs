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
    private DogfightAnimation currentAnimation = DogfightAnimation.None;

    private GameObject drawnCard1;
    private GameObject drawnCard2;

    private AnimationHelper animationHelper = new AnimationHelper();


    // Start is called before the first frame update
    void Start()
    {
        HandleDogfightStageChange();
    }

    // Update is called once per frame
    void Update()
    {
         // animate something if I should
         switch (currentAnimation)
        {
            case DogfightAnimation.None:
                break;
            case DogfightAnimation.DrawCard:
                DrawCardAnimation();
                break;
        }
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
        drawnCard1 = Instantiate(
            crewCardPrefab,
            new Vector3(DogfightConstants.deck1X, DogfightConstants.deck1Y, transform.position.z),
            transform.rotation);

        crewCardPrefab.GetComponent<CrewCardScript>().crewCard = deck2[0];
        drawnCard2 = Instantiate(
            crewCardPrefab,
            new Vector3(DogfightConstants.deck2X, DogfightConstants.deck2Y, transform.position.z),
            transform.rotation);

        //make the cards get bigger
        currentAnimation = DogfightAnimation.DrawCard;
    }

    void DrawCardAnimation()
    {
        if (animationHelper.NotYetReachedDestination(new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY), drawnCard1) ||
            animationHelper.NotYetReachedDestination(new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY), drawnCard2) ||
            animationHelper.NotYetReachedScale(DogfightConstants.viewCardScaleSize, drawnCard1))
        {
            Vector3 newScaleValue = animationHelper.ScaleTowardsSize(DogfightConstants.viewCardScaleSize, 1f, 1000f, drawnCard1);
            drawnCard1.transform.localScale = newScaleValue;
            drawnCard2.transform.localScale = newScaleValue;

            drawnCard1.transform.position = animationHelper.MoveTowardsPoint(new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY), new Vector3(DogfightConstants.deck1X, DogfightConstants.deck1Y), DogfightConstants.viewCardAnimationTime, drawnCard1);
            drawnCard2.transform.position = animationHelper.MoveTowardsPoint(new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY), new Vector3(DogfightConstants.deck2X, DogfightConstants.deck2Y), DogfightConstants.viewCardAnimationTime, drawnCard2);
        } else
        {
            currentAnimation = DogfightAnimation.None;
        }
        
    }
}
