#TODO
# - properly implement the built in intents
import json
import challonge

USER = "haydunce" 
KEY = "yCYu1uKVX10iNrRh5vJfy48ReZC2iQ0Kchi4xzMs"
TOURNAMENT_NAME = "HackAZ"

challonge.set_credentials(USER, KEY)
tournament = challonge.tournaments.show(TOURNAMENT_NAME)
participants = challonge.participants.index(tournament['id'])
matches = challonge.matches.index(tournament['id'])

#Custom Intents Functions
#-------------------------------------------------------
def start_tournament():
    global tournament
    challonge.tournaments.start(tournament["id"])
    return statement("Tournament Started","The tournament has started")

def reset_tournament():
    global tournament
    challonge.tournaments.reset(tournament['id'])
    return statement("Tournament Reset","The tournament has been reset")

def get_num_participants():
    global participants
    return statement("Number of Participants","There are " + str(len(participants)) + " participants")

#returns null if not found
def get_participant_from_id(id):
    global participants
    for p in (participants):
        if p['id'] == id:
            return p['name']
    return None

#returns null if not found
def get_id_from_participant(name):
    global participants
    for p in (participants):
        if p['name'] == name:
            return p['id']
    return None

#returns the current match of specified type
def get_match_from_state(match_type= "open"):
    global matches
    for m in matches:
        if(m['state'] == match_type):
            return m  #returns id (integer) of the match

def match_id_to_match(match_id):
    global matches
    for m in matches:
        if(m['id'] == match_id):
            return m  #returns match

def next_open_match():
    global matches
    global participants
    current_match = 0
    count = 1
    for m in matches:
        if(m['state'] == "open"):
            current_match = m
            break
        count+=1
    player1 = get_participant(current_match['player1_id'])
    player2 = get_participant(current_match['player2_id'])
    return statement("Next Match",("The next match is match " + str(count) + " between " + player1 + " and " + player2))

#attempts to set the completed score/outcome
def update_match(match_id, winner_id, scores = ""):
    global matches
    current_match = match_id_to_match(match_id)
    winner = get_participant_from_id(winner_id)
    current_match.report_winner(winner, scores)

    return matches
    

#combines the information into an actual response

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
    
    if intent == "NextMatch":
        return next_open_match()

    if intent == "NumberOfParticipants":
        return get_num_participants()

    if intent == "ResetTournament":
        return reset_tournament()

#Built in Intents Functions
#-------------------------------------------------------
def cancel_intent():
    return statement("cancel","You want to cancel")
def help_intent():
    return statement("help","You want help")
def stop_intent():
    return statement("stop","You want to stop")

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
    speechlet['card'] = build_SimpleCard(title, body)
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

#Methods for testing
def get_matches():
    global matches
    return matches

#def main():
#    reset_tournament()
#    start_tournament()
#    print(get_matches())
#    print("============================================")
#    match1 = get_match_from_state()
#    print(update_match(match1['id'], match1['player1_id'], "1-2,3-6"))
#    print("============================================")
#    match2 = get_match_from_state()
#    print(update_matches(match2['id'], match2['player1_id'], "3-1, 7-3"))
#
#main()