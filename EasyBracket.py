import json
import challonge
import asyncio

tournament = None
participants = []
matches = None

async def login(tournament_name = "HackAZ"):
    global tournament
    global participants
    global matches

    USER = "haydunce" 
    KEY = "yCYu1uKVX10iNrRh5vJfy48ReZC2iQ0Kchi4xzMs"

    user = await challonge.get_user(USER, KEY)
    tournament = await user.get_tournament(url = tournament_name)
    participants = await tournament.get_participants()
    matches = await tournament.get_matches()



#Custom Intents Functions
#-------------------------------------------------------
async def start_tournament():
    global tournament
    await tournament.start()
    return statement("Tournament Started","The tournament has started")

async def reset_tournament():
    global tournament
    await tournament.reset()
    return statement("Tournament Reset","The tournament has been reset")

async def get_num_participants():
    global participants
    return statement("Number of Participants","There are " + str(len(participants)) + " participants")

#returns null if not found
async def get_id_from_participant(name):
    global participants
    for p in (participants):
        print(p.name)
        if p.name == name:
            return p.id
    return None

async def get_next_match():
    global tournament
    current_match = None

    for m in matches:
        if(m.state == "open"):
            current_match = m

    return current_match

async def next_open_match():
    current_match = await get_next_match()

    player1 = await tournament.get_participant(current_match.player1_id)
    player2 = await tournament.get_participant(current_match.player2_id)

    return statement("Next Match",("The next match is between " + player1 + " and " + player2))

#attempts to set the completed score/outcome
async def update_match(match_id, winner_id, scores = ""):
    global tournament
    winner = await tournament.get_participant(winner_id)
    match = await tournament.get_match(match_id)
    await match.report_winner(winner, scores)
    
    return None
    

#combines the information into an actual response

async def lambda_handler(event, context):
    await login()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)

def on_launch(event, context):
    return statement("Bracketier","something works")

async def intent_router(event, context):
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
        return await start_tournament()
    
    if intent == "NextMatch":
        return await next_open_match()

    if intent == "NumberOfParticipants":
        return await get_num_participants()

    if intent == "ResetTournament":
        return await reset_tournament()

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

async def main(loop):
    global tournament
    await login()
    p = await get_id_from_participant('Jose')
    print(p)
    print('=====================================================')
    print(get_matches())
    print("=====================================================")
    match1 = await get_next_match()
    print(await update_match(match1.id, match1.player1_id, "1-2,3-6"))
    print("=====================================================")
    match2 = await get_next_match()
    print(await update_match(match2.id, match2.player1_id, "3-1, 7-3"))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))