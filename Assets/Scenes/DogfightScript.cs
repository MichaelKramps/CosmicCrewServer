using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;
using TMPro;

public class DogfightScript : MonoBehaviour
{
    public GameObject crewCardPrefab;
    public GameObject diePrefab;
    //has all cards in the game 
    public List<CrewCard> crewCards;

    //related to gameplay
    private Player player1 = new Player();
    private Player player2 = new Player();

    private GameObject activeCard1;
    private GameObject activeCard2;
    private GameObject die1;
    private GameObject die2;

    //related to animation
    private Queue<DogfightAnimation> animationQueue = new Queue<DogfightAnimation>();
    private AnimationHelper animationHelper = new AnimationHelper();


    // Start is called before the first frame update
    void Start()
    {
        //load decks with cards
        player1.addCardToDeck(cardWithId(0, 1));
        player1.addCardToDeck(cardWithId(1, 1));
        player1.addCardToDeck(cardWithId(2, 1));
        player1.addCardToDeck(cardWithId(2, 1));
        player1.addCardToDeck(cardWithId(1, 1));
        player1.addCardToDeck(cardWithId(0, 1));
        player2.addCardToDeck(cardWithId(0, 2));
        player2.addCardToDeck(cardWithId(1, 2));
        player2.addCardToDeck(cardWithId(2, 2));
        player2.addCardToDeck(cardWithId(0, 2));
        player2.addCardToDeck(cardWithId(1, 2));
        player2.addCardToDeck(cardWithId(2, 2));
        //Queue all animations
        animationQueue = new FightAutomator().getFightAnimations();
        //Outcome of fight will be determined by server

    }

    // Update is called once per frame
    void Update()
    {
        DogfightAnimation currentAnimation = animationQueue.Count > 0 ? animationQueue.Peek() : new DogfightAnimation(DogfightAnimationType.EndFight);
         // animate something if I should
         switch (currentAnimation.getAnimationType())
        {
            case DogfightAnimationType.None:
                NextAnimation();
                break;
            case DogfightAnimationType.Wait:
                WaitAnimation(currentAnimation.getIntegerValue());
                break;
            case DogfightAnimationType.DrawCard:
                DrawCard(currentAnimation);
                break;
            case DogfightAnimationType.ShowCard:
                ShowCardAnimation();
                break;
            case DogfightAnimationType.PlayCard:
                PlayCardAnimation(currentAnimation);
                break;
            case DogfightAnimationType.ShowDice:
                ShowDiceAnimation();
                break;
            case DogfightAnimationType.RollDice:
                RollDiceAnimation(currentAnimation.getIntegerValue(), currentAnimation.getSecondIntegerValue());
                break;
            case DogfightAnimationType.HideDice:
                HideDiceAnimation();
                break;
            case DogfightAnimationType.SelectFighter:
                SelectFighterAnimation(currentAnimation.getIntegerValue(), currentAnimation.getSecondIntegerValue());
                break;
            case DogfightAnimationType.SingleFightTies:
                SingleFightTiesAnimation(currentAnimation.getIntegerValue(), currentAnimation.getSecondIntegerValue());
                break;
            case DogfightAnimationType.NormalPlayer1Win:
            case DogfightAnimationType.EmptyDeckPlayer1Win:
                SingleFightPlayer1WinsAnimation(currentAnimation.getIntegerValue(), currentAnimation.getSecondIntegerValue());
                break;
            case DogfightAnimationType.NormalPlayer2Win:
            case DogfightAnimationType.EmptyDeckPlayer2Win:
                SingleFightPlayer2WinsAnimation(currentAnimation.getIntegerValue(), currentAnimation.getSecondIntegerValue());
                break;
            case DogfightAnimationType.EndFight:
                SceneManager.LoadScene("MainMenu");
                break;

        }
    }

    GameObject cardWithId(int idOfCard, int playerNumber)
    {
        crewCardPrefab.GetComponent<CrewCardScript>().crewCard = crewCards[idOfCard];
        return Instantiate(
            crewCardPrefab,
            new Vector3(DogfightConstants.deck1X, DogfightConstants.deck1Y, transform.position.z),
            transform.rotation);
    }

    void DrawCard(DogfightAnimation dogfightAnimation)
    {
        switch (dogfightAnimation.getActingPlayer())
        {
            case ActingPlayer.Primary:
                activeCard1 = player1.drawCard();
                break;
            case ActingPlayer.Secondary:
                activeCard2 = player2.drawCard();
                break;
            case ActingPlayer.Both:
                activeCard1 = player1.drawCard();
                activeCard2 = player2.drawCard();
                break;
        }

        NextAnimation();
    }

    void WaitAnimation(int millisecondsToWait)
    {
        bool finishedWaiting = animationHelper.waitForMilliseconds(millisecondsToWait);
        if (finishedWaiting)
        {
            NextAnimation();
        }
    }

    void ShowCardAnimation()
    {
        Vector3 cardViewDestination1 = new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY);
        Vector3 cardViewDestination2 = new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY);
        if (animationHelper.NotYetReachedDestination(new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY), activeCard1) ||
            animationHelper.NotYetReachedDestination(new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY), activeCard2) ||
            animationHelper.NotYetReachedScale(DogfightConstants.viewCardScaleSize, activeCard1))
        {
            Vector3 newScaleValue = animationHelper.ScaleTowardsSize(DogfightConstants.viewCardScaleSize, 1f, DogfightConstants.viewCardAnimationTime, activeCard1);
            activeCard1.transform.localScale = newScaleValue;
            activeCard2.transform.localScale = newScaleValue;

            activeCard1.transform.position = animationHelper.MoveTowardsPoint(cardViewDestination1, new Vector3(DogfightConstants.deck1X, DogfightConstants.deck1Y), DogfightConstants.viewCardAnimationTime, activeCard1);
            activeCard2.transform.position = animationHelper.MoveTowardsPoint(cardViewDestination2, new Vector3(DogfightConstants.deck2X, DogfightConstants.deck2Y), DogfightConstants.viewCardAnimationTime, activeCard2);
        } else
        {
            NextAnimation();
        }
        
    }

    void PlayCardAnimation(DogfightAnimation animation)
    {
        //card is being viewed
        //move to correct slot
        Vector3 cardDestination1 = new Vector3(DogfightConstants.gunner1XStart + ((animation.getIntegerValue() - 1) * 2.5f), DogfightConstants.gunner1Y);
        Vector3 cardDestination2 = new Vector3(DogfightConstants.gunner2XStart + ((animation.getSecondIntegerValue() - 1) * 2.5f), DogfightConstants.gunner2Y);
        Vector3 cardOrigination1 = new Vector3(DogfightConstants.deck1X, DogfightConstants.deck1Y);
        Vector3 cardOrigination2 = new Vector3(DogfightConstants.deck2X, DogfightConstants.deck2Y);
        switch (animation.getActingPlayer())
        {
            case ActingPlayer.Primary:
                if (animationHelper.NotYetReachedDestination(cardDestination1, activeCard1))
                {
                    activeCard1.transform.position = animationHelper.MoveTowardsPoint(cardDestination1, cardOrigination1, DogfightConstants.viewCardAnimationTime, activeCard1);
                }
                else
                {
                    player1.playCard(activeCard1);
                    NextAnimation();
                }
                break;
            case ActingPlayer.Secondary:
                if (animationHelper.NotYetReachedDestination(cardDestination2, activeCard2))
                {
                    activeCard2.transform.position = animationHelper.MoveTowardsPoint(cardDestination2, cardOrigination2, DogfightConstants.viewCardAnimationTime, activeCard2);
                }
                else
                {
                    player2.playCard(activeCard2);
                    NextAnimation();
                }
                break;
            case ActingPlayer.Both:
                if (animationHelper.NotYetReachedDestination(cardDestination1, activeCard1) ||
                    animationHelper.NotYetReachedDestination(cardDestination2, activeCard2))
                {
                    activeCard1.transform.position = animationHelper.MoveTowardsPoint(cardDestination1, cardOrigination1, DogfightConstants.viewCardAnimationTime, activeCard1);
                    activeCard2.transform.position = animationHelper.MoveTowardsPoint(cardDestination2, cardOrigination2, DogfightConstants.viewCardAnimationTime, activeCard2);
                }
                else
                {
                    player1.playCard(activeCard1);
                    player2.playCard(activeCard2);
                    NextAnimation();
                }
                break;
        }
    }

    void ShowDiceAnimation()
    {
        die1 = Instantiate(
            diePrefab,
            new Vector3(DogfightConstants.die1X, DogfightConstants.die1Y, transform.position.z),
            transform.rotation);
        die2 = Instantiate(
            diePrefab,
            new Vector3(DogfightConstants.die2X, DogfightConstants.die2Y, transform.position.z),
            transform.rotation);
        NextAnimation();
    }

    void HideDiceAnimation()
    {
        Destroy(die1);
        Destroy(die2);
        NextAnimation();
    }

    void RollDiceAnimation(int numberRolled1, int numberRolled2)
    {
        bool finishedWaiting = animationHelper.waitForMilliseconds(1500);
        die1.GetComponentInChildren<TextMeshPro>().text = Random.Range(1, 6).ToString();
        die2.GetComponentInChildren<TextMeshPro>().text = Random.Range(1, 6).ToString();
        if (finishedWaiting)
        {
            die1.GetComponentInChildren<TextMeshPro>().text = numberRolled1.ToString();
            die2.GetComponentInChildren<TextMeshPro>().text = numberRolled2.ToString();
            NextAnimation();
        }
    }

    void SelectFighterAnimation(int fighterRolled1, int fighterRolled2)
    {
        GameObject fighter1Selected = player1.gunnerFromRoll(fighterRolled1);
        GameObject fighter2Selected = player2.gunnerFromRoll(fighterRolled2);
        fighter1Selected.GetComponent<SortingGroup>().sortingLayerName = "Over Cards";
        fighter2Selected.GetComponent<SortingGroup>().sortingLayerName = "Over Cards";
        Vector3 cardViewDestination1 = new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY);
        Vector3 cardViewDestination2 = new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY);
        Vector3 cardOrigination1 = new Vector3(DogfightConstants.gunner1XStart + ((player1.indexOfFirstAvailableGunner(fighterRolled1)) * 2.5f), DogfightConstants.gunner1Y);
        Vector3 cardOrigination2 = new Vector3(DogfightConstants.gunner2XStart + ((player2.indexOfFirstAvailableGunner(fighterRolled2)) * 2.5f), DogfightConstants.gunner2Y);
        if (animationHelper.NotYetReachedDestination(cardViewDestination1, fighter1Selected) ||
            animationHelper.NotYetReachedDestination(cardViewDestination2, fighter2Selected) ||
            animationHelper.NotYetReachedScale(DogfightConstants.viewCardScaleSize, fighter1Selected))
        {
            Vector3 newScaleValue = animationHelper.ScaleTowardsSize(DogfightConstants.viewCardScaleSize, 1f, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter1Selected.transform.localScale = newScaleValue;
            fighter2Selected.transform.localScale = newScaleValue;

            fighter1Selected.transform.position = animationHelper.MoveTowardsPoint(cardViewDestination1, cardOrigination1, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter2Selected.transform.position = animationHelper.MoveTowardsPoint(cardViewDestination2, cardOrigination2, DogfightConstants.viewCardAnimationTime, fighter2Selected);
        }
        else
        {
            NextAnimation();
        }

    }

    void SingleFightTiesAnimation(int fighterRolled1, int fighterRolled2)
    {
        GameObject fighter1Selected = player1.gunnerFromRoll(fighterRolled1);
        fighter1Selected.GetComponentInChildren<SpriteRenderer>().color = Color.red;
        GameObject fighter2Selected = player2.gunnerFromRoll(fighterRolled2);
        fighter2Selected.GetComponentInChildren<SpriteRenderer>().color = Color.red;
        Vector3 cardDestination1 = new Vector3(DogfightConstants.discard1X, DogfightConstants.discard1Y);
        Vector3 cardDestination2 = new Vector3(DogfightConstants.discard2X, DogfightConstants.discard2Y);
        Vector3 cardOrigination1 = new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY);
        Vector3 cardOrigination2 = new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY);
        if (animationHelper.NotYetReachedDestination(cardDestination1, fighter1Selected) ||
            animationHelper.NotYetReachedDestination(cardDestination2, fighter2Selected) ||
            animationHelper.NotYetReachedScale(1f, fighter1Selected))
        {
            Vector3 newScaleValue = animationHelper.ScaleTowardsSize(1f, DogfightConstants.viewCardScaleSize, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter1Selected.transform.localScale = newScaleValue;
            fighter2Selected.transform.localScale = newScaleValue;

            fighter1Selected.transform.position = animationHelper.MoveTowardsPoint(cardDestination1, cardOrigination1, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter2Selected.transform.position = animationHelper.MoveTowardsPoint(cardDestination2, cardOrigination2, DogfightConstants.viewCardAnimationTime, fighter2Selected);
        }
        else
        {
            fighter1Selected.GetComponent<SortingGroup>().sortingLayerName = "Cards";
            fighter1Selected.GetComponentInChildren<SpriteRenderer>().color = Color.white;
            fighter2Selected.GetComponent<SortingGroup>().sortingLayerName = "Cards";
            fighter2Selected.GetComponentInChildren<SpriteRenderer>().color = Color.white;
            player1.discardGunner(fighterRolled1);
            player2.discardGunner(fighterRolled2);
            NextAnimation();
        }
    }

    void SingleFightPlayer1WinsAnimation(int fighterRolled1, int fighterRolled2)
    {
        GameObject fighter1Selected = player1.gunnerFromRoll(fighterRolled1);
        fighter1Selected.GetComponentInChildren<SpriteRenderer>().color = Color.green;
        GameObject fighter2Selected = player2.gunnerFromRoll(fighterRolled2);
        fighter2Selected.GetComponentInChildren<SpriteRenderer>().color = Color.red;
        Vector3 cardDestination1 = new Vector3(DogfightConstants.deck1X, DogfightConstants.deck1Y);
        Vector3 cardDestination2 = new Vector3(DogfightConstants.discard2X, DogfightConstants.discard2Y);
        Vector3 cardOrigination1 = new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY);
        Vector3 cardOrigination2 = new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY);
        if (animationHelper.NotYetReachedDestination(cardDestination1, fighter1Selected) ||
            animationHelper.NotYetReachedDestination(cardDestination2, fighter2Selected) ||
            animationHelper.NotYetReachedScale(1f, fighter1Selected))
        {
            Vector3 newScaleValue = animationHelper.ScaleTowardsSize(1f, DogfightConstants.viewCardScaleSize, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter1Selected.transform.localScale = newScaleValue;
            fighter2Selected.transform.localScale = newScaleValue;

            fighter1Selected.transform.position = animationHelper.MoveTowardsPoint(cardDestination1, cardOrigination1, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter2Selected.transform.position = animationHelper.MoveTowardsPoint(cardDestination2, cardOrigination2, DogfightConstants.viewCardAnimationTime, fighter2Selected);
        }
        else
        {
            player1.putGunnerAtBottomOfDeck(fighterRolled1);
            player2.discardGunner(fighterRolled2);
            fighter1Selected.GetComponent<SortingGroup>().sortingLayerName = "Cards";
            fighter1Selected.GetComponentInChildren<SpriteRenderer>().color = Color.white;
            fighter2Selected.GetComponent<SortingGroup>().sortingLayerName = "Cards";
            fighter2Selected.GetComponentInChildren<SpriteRenderer>().color = Color.white;
            NextAnimation();
        }
    }

    void SingleFightPlayer2WinsAnimation(int fighterRolled1, int fighterRolled2)
    {
        GameObject fighter1Selected = player1.gunnerFromRoll(fighterRolled1);
        fighter1Selected.GetComponentInChildren<SpriteRenderer>().color = Color.red;
        GameObject fighter2Selected = player2.gunnerFromRoll(fighterRolled2);
        fighter2Selected.GetComponentInChildren<SpriteRenderer>().color = Color.green;
        Vector3 cardDestination1 = new Vector3(DogfightConstants.discard1X, DogfightConstants.discard1Y);
        Vector3 cardDestination2 = new Vector3(DogfightConstants.deck2X, DogfightConstants.deck2Y);
        Vector3 cardOrigination1 = new Vector3(DogfightConstants.card1ViewCardX, DogfightConstants.card1ViewCardY);
        Vector3 cardOrigination2 = new Vector3(DogfightConstants.card2ViewCardX, DogfightConstants.card2ViewCardY);
        if (animationHelper.NotYetReachedDestination(cardDestination1, fighter1Selected) ||
            animationHelper.NotYetReachedDestination(cardDestination2, fighter2Selected) ||
            animationHelper.NotYetReachedScale(1f, fighter1Selected))
        {
            Vector3 newScaleValue = animationHelper.ScaleTowardsSize(1f, DogfightConstants.viewCardScaleSize, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter1Selected.transform.localScale = newScaleValue;
            fighter2Selected.transform.localScale = newScaleValue;

            fighter1Selected.transform.position = animationHelper.MoveTowardsPoint(cardDestination1, cardOrigination1, DogfightConstants.viewCardAnimationTime, fighter1Selected);
            fighter2Selected.transform.position = animationHelper.MoveTowardsPoint(cardDestination2, cardOrigination2, DogfightConstants.viewCardAnimationTime, fighter2Selected);
        }
        else
        {
            player1.discardGunner(fighterRolled1);
            player2.putGunnerAtBottomOfDeck(fighterRolled2);
            fighter1Selected.GetComponent<SortingGroup>().sortingLayerName = "Cards";
            fighter1Selected.GetComponentInChildren<SpriteRenderer>().color = Color.white;
            fighter2Selected.GetComponent<SortingGroup>().sortingLayerName = "Cards";
            fighter2Selected.GetComponentInChildren<SpriteRenderer>().color = Color.white;
            NextAnimation();
        }
    }

    void NextAnimation()
    {
        animationQueue.Dequeue();
    }
}
