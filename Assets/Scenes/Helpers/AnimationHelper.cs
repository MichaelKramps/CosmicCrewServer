using System;
using UnityEngine;

public class AnimationHelper
{
    public AnimationHelper()
    {
    }

    public Vector3 MoveTowardsPoint(Vector3 destination, Vector3 startingPoint, float timeInMilliseconds, GameObject objectToMove)
    {
        if (NotYetReachedDestination(destination, objectToMove))
        {
            float currentX = objectToMove.transform.position.x;
            float currentY = objectToMove.transform.position.y;

            float amountToChangeX = ((destination.x - startingPoint.x) / (timeInMilliseconds / 1000f)) * Time.deltaTime;
            float amountToChangeY = ((destination.y - startingPoint.y) / (timeInMilliseconds / 1000f)) * Time.deltaTime;

            float newX = currentX + amountToChangeX;
            float newY = currentY + amountToChangeY;


            if ((destination.x > startingPoint.x && newX > destination.x) || (destination.x < startingPoint.x && newX < destination.x))
            {
                newX = destination.x;
            }

            if ((destination.y > startingPoint.y && newY > destination.y) || (destination.y < startingPoint.y && newY < destination.y))
            {
                newY = destination.y;
            }

            return new Vector3(newX, newY, objectToMove.transform.position.z);
        }
        else
        {
            return destination;
        }

    }

    public bool NotYetReachedDestination(Vector3 destination, GameObject objectToMove)
    {
        return objectToMove.transform.position.x != destination.x || objectToMove.transform.position.y != destination.y;
    }

    public Vector3 ScaleTowardsSize(float scaleDestination, float scaleStartingPoint, float timeInMilliseconds, GameObject objectToScale)
    {
        if (NotYetReachedScale(scaleDestination, objectToScale))
        {
            float currentScaleValue = objectToScale.transform.localScale.x;
            float scaleBase = (scaleDestination - scaleStartingPoint) / (timeInMilliseconds / 1000f);
            float amountToScale = 1f + (scaleBase * Time.deltaTime);

            float newScaleValue = currentScaleValue * amountToScale;

            if (scaleDestination > scaleStartingPoint && newScaleValue > scaleDestination)
            {
                newScaleValue = scaleDestination;
            }
            else if (scaleDestination < scaleStartingPoint && newScaleValue < scaleDestination)
            {
                newScaleValue = scaleDestination;
            }

            return new Vector3(newScaleValue, newScaleValue);
        }
        else
        {
            return objectToScale.transform.localScale;
        }

    }

    public bool NotYetReachedScale(float destination, GameObject objectToMove)
    {
        return objectToMove.transform.localScale.x != destination;
    }
}
