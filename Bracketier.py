#TODO
# - properly implement the built in intents

import challonge

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
def next_match(event, context):
    #code to access the Challonge API here
    return message("Next Match","The next match is number"+nextMatchNum)

def ongoing_matches(event, context):
    #code to access the Challonge API here

#helper method, builds a card
def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['text'] = body
    return card

#combines the information into an actual response
def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    respons['response'] = message
    return response
