#TODO
# - properly implement the built in intents

import json
import challonge

challonge.set_credentials("haydunce","yCYu1uKVX10iNrRh5vJfy48ReZC2iQ0Kchi4xzMs")

tournament = challonge.tournaments.show("HackAZ")

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)

def on_launch(event, context):
    return statement("Bracketier","something works")

def intent_router(event, context):
    intent = event['request']['intent']['name']
    
    #required intents 
    if intent == "AMAZON.CancelIntent":
        return cancel_intent()
    
    if intent == "AMAZON.HelpIntent":
        return help_intent()
    
    if intent == "AMAZON.StopIntent":
        return stop_itent()

    #custom intents

    if intent == "StartTournament":
        return start_tournament()

#Built in Intents Functions
#-------------------------------------------------------
def cancel_intent():
    return statement("cancel","You want to cancel")
def help_intent():
    return statement("help","You want help")
def stop_intent():
    return statement("stop","You want to stop")

#Custom Intents Functions
#-------------------------------------------------------
def start_tournament():
    challonge.tournaments.start(tournament["id"])
    return statement("Tournament Start", "The tournaments has started")


# usedul builder stuff

def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

def conversation(title, body, session_attrs):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet{'card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes = session_attrs)

def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card
