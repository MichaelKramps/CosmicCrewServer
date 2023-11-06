using System;
using System.Collections.Generic;

//this class is sort of mocking the server for now
//the server will ultimately be sending the animation codes and the result of a fight
public class FightAutomator
{
    CrewDeck deck1;
    CrewDeck deck2;

    Queue<DogfightAnimation> fightAnimations = new Queue<DogfightAnimation>();

    public FightAutomator()
    {
    }

    public FightAutomator(CrewDeck deck1, CrewDeck deck2)
    {
        this.deck1 = deck1;
        this.deck2 = deck2;
    }

    public Queue<DogfightAnimation> getFightAnimations()
    {
        if (this.fightAnimations.Count > 0)
        {
            return this.fightAnimations;
        } else
        {
            Queue<String> animationCodesFromServer = new Queue<String>();
            animationCodesFromServer.Enqueue("b,d6,0,0");//code for drawing 6 cards at start of battle
            animationCodesFromServer.Enqueue("b,r,3,5");//player1 rolls a 3 and player2 rolls a 5
            animationCodesFromServer.Enqueue("b,1ew,3,5");
            animationCodesFromServer.Enqueue("b,r,3,5");
            animationCodesFromServer.Enqueue("b,sft,3,5");
            animationCodesFromServer.Enqueue("b,r,3,5");
            animationCodesFromServer.Enqueue("b,sft,3,5");
            //animationCodesFromServer.Enqueue("b,r,6,1");
            //animationCodesFromServer.Enqueue("b,sft,6,1");
            //animationCodesFromServer.Enqueue("b,r,2,4");
            //animationCodesFromServer.Enqueue("b,1nw,2,4");
            //animationCodesFromServer.Enqueue("b,r,1,2");
            //animationCodesFromServer.Enqueue("b,2ew,1,2");
            //animationCodesFromServer.Enqueue("b,r,5,3");
            //animationCodesFromServer.Enqueue("b,2nw,5,3");
            //animationCodesFromServer.Enqueue("b,r,4,6");
            //animationCodesFromServer.Enqueue("b,sft,4,6");
            return createFightAnimations(animationCodesFromServer);
        }
    }

    public Queue<DogfightAnimation> createFightAnimations(Queue<String> codesFromServer)
    {
        Queue<DogfightAnimation> animations = new Queue<DogfightAnimation>();

        while(codesFromServer.Count > 0)
        {
            AddAnimationsFromServerAnimationCodes(animations, codesFromServer.Dequeue());
        }

        return animations;
    }

    void AddAnimationsFromServerAnimationCodes(Queue<DogfightAnimation> animations, String codeFromServer)
    {
        String[] splitCodes = codeFromServer.Split(",");
        switch(splitCodes[1])
        {
            case "d6":
                animations.Enqueue(new DogfightAnimation("b,d,0,0"));//both players draw a card
                animations.Enqueue(new DogfightAnimation("b,p,1,1"));//both players play a card in position 1
                animations.Enqueue(new DogfightAnimation("b,d,0,0"));
                animations.Enqueue(new DogfightAnimation("b,p,2,2"));//both players play a card in position 2
                animations.Enqueue(new DogfightAnimation("b,d,0,0"));
                animations.Enqueue(new DogfightAnimation("b,p,3,3"));
                animations.Enqueue(new DogfightAnimation("b,d,0,0"));
                animations.Enqueue(new DogfightAnimation("b,p,4,4"));
                animations.Enqueue(new DogfightAnimation("b,d,0,0"));
                animations.Enqueue(new DogfightAnimation("b,p,5,5"));
                animations.Enqueue(new DogfightAnimation("b,d,0,0"));
                animations.Enqueue(new DogfightAnimation("b,p,6,6"));
                animations.Enqueue(new DogfightAnimation("b,w,700,0"));
                break;
            case "r":
                animations.Enqueue(new DogfightAnimation("b,sd,0,0"));
                animations.Enqueue(new DogfightAnimation("b,w,700,0"));
                animations.Enqueue(new DogfightAnimation(codeFromServer));
                animations.Enqueue(new DogfightAnimation("b,w,1200,0"));
                animations.Enqueue(new DogfightAnimation("b,hd,0,0"));
                animations.Enqueue(new DogfightAnimation("b,sf," + splitCodes[2] + "," + splitCodes[3]));
                animations.Enqueue(new DogfightAnimation("b,w,1500,0"));
                break;
            case "sft":
                animations.Enqueue(new DogfightAnimation(codeFromServer));
                animations.Enqueue(new DogfightAnimation("b,w,700,0"));
                break;
            case "1nw":
                animations.Enqueue(new DogfightAnimation(codeFromServer));
                animations.Enqueue(new DogfightAnimation("p,d,0,0"));
                animations.Enqueue(new DogfightAnimation("p,p," + splitCodes[2] + ",0"));
                animations.Enqueue(new DogfightAnimation("b,w,700,0"));
                break;
            case "2nw":
                animations.Enqueue(new DogfightAnimation(codeFromServer));
                animations.Enqueue(new DogfightAnimation("s,d,0,0"));
                animations.Enqueue(new DogfightAnimation("s,p,0," + splitCodes[3]));
                animations.Enqueue(new DogfightAnimation("b,w,700,0"));
                break;
            case "1ew":
            case "2ew":
                animations.Enqueue(new DogfightAnimation(codeFromServer));
                animations.Enqueue(new DogfightAnimation("b,w,700,0"));
                break;
            default:
                animations.Enqueue(new DogfightAnimation(codeFromServer));
                break;
        }
    }
}
