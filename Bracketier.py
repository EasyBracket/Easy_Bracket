#TODO
# - properly implement the built in intents

import challonge

challonge.set_credentials("haydunce","yCYu1uKVX10iNrRh5vJfy48ReZC2iQ0Kchi4xzMs")

tournament = challonge.tournaments.show("HackAZ")

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
    if intent == "NextMatch":
        return next_match()

    if intent == "StartTournmaent":
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
def on_launch(event, context):
    return statement("Bracket Status", "")

def start_tournament():
    challonge.tournaments.start(tournament["id"])
    return message("Tournament Start", "The tournaments has started")

def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build _PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

#helper method, creates a dictionary 
def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['text'] = body
    return card

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    respons['response'] = message
    return response
