import json
from DogfightSimulator import DogfightSimulator
from Player import Player
from Animations import Animations

def lambda_handler(event, context):
    # TODO implement
    animations = Animations()
    simulator = DogfightSimulator(event["deckOne"], event["deckTwo"], animations)
    simulator.simulateDogfight()
    return {
        'statusCode': 200,
        'body': {
            'startingDeckOne': simulator.startingDeckOne,
            'startingDeckTwo': simulator.startingDeckTwo,
            'animationString': '*'.join(animations.animationsList)
        }
    }
