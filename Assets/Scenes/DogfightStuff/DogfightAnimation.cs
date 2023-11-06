using System;
public class DogfightAnimation
{
    DogfightAnimationType animationType = DogfightAnimationType.None;
    ActingPlayer actingPlayer = ActingPlayer.None;
    int integerValue = 0;
    int secondIntegerValue = 0;

    public DogfightAnimation()
    {
        this.animationType = DogfightAnimationType.None;
    }

    public DogfightAnimation(DogfightAnimationType type)
    {
        this.animationType = type;
    }

    public DogfightAnimation(DogfightAnimationType type, int intValue)
    {
        this.animationType = type;
        this.integerValue = intValue;
    }

    public DogfightAnimation(String animationCodeString)
    {
        //animationCodeString should have a format like "a,b,c,d"
        String[] animationCodeArray = animationCodeString.Split(",");
        //each comma separated value determines a different characteristic of the animation
        this.actingPlayer = determineActingPlayer(animationCodeArray[0]);
        this.animationType = determineAnimationType(animationCodeArray[1]);
        this.integerValue = determineIntegerValue(animationCodeArray[2]);
        this.secondIntegerValue = determineIntegerValue(animationCodeArray[3]);
    }

    public ActingPlayer getActingPlayer()
    {
        return actingPlayer;
    }

    public DogfightAnimationType getAnimationType()
    {
        return this.animationType;
    }

    public int getIntegerValue()
    {
        return this.integerValue;
    }

    public int getSecondIntegerValue()
    {
        return this.secondIntegerValue;
    }

    private ActingPlayer determineActingPlayer (String code)
    {
        switch (code.ToLower())
        {
            case "p":
                return ActingPlayer.Primary;
            case "s":
                return ActingPlayer.Secondary;
            case "b":
                return ActingPlayer.Both;
            default:
                return ActingPlayer.None;
        }
    }

    private DogfightAnimationType determineAnimationType(String code)
    {
        switch(code.ToLower())
        {
            case "d":
                return DogfightAnimationType.DrawCard;
            case "hd":
                return DogfightAnimationType.HideDice;
            case "p":
                return DogfightAnimationType.PlayCard;
            case "r":
                return DogfightAnimationType.RollDice;
            case "sc":
                return DogfightAnimationType.ShowCard;
            case "sd":
                return DogfightAnimationType.ShowDice;
            case "sf":
                return DogfightAnimationType.SelectFighter;
            case "sft":
                return DogfightAnimationType.SingleFightTies;
            case "1nw":
                return DogfightAnimationType.NormalPlayer1Win;
            case "2nw":
                return DogfightAnimationType.NormalPlayer2Win;
            case "1ew":
                return DogfightAnimationType.EmptyDeckPlayer1Win;
            case "2ew":
                return DogfightAnimationType.EmptyDeckPlayer2Win;
            case "w":
                return DogfightAnimationType.Wait;
            default:
                return DogfightAnimationType.None;
        }
    }

    private int determineIntegerValue(String code)
    {
        try
        {
            int parsedInteger = Int32.Parse(code);
            return parsedInteger;
        } catch
        {
            return 0;
        }
    }
}

public enum ActingPlayer
{
    Primary,
    Secondary,
    Both,
    None
}

public enum DogfightAnimationType
{
    None,
    Wait,
    DrawCard,
    ShowCard,
    PlayCard,
    ShowDice,
    RollDice,
    HideDice,
    SelectFighter,
    SingleFightTies,
    NormalPlayer1Win,
    NormalPlayer2Win,
    EmptyDeckPlayer1Win,
    EmptyDeckPlayer2Win,
    EndFight
}
