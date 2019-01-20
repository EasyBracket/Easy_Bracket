import json
import challonge
import asyncio

tournament = None
participants = []
matches = None
names = []

#Startup
#--------------------------------------------------
async def login(tournament_name = "HackAZ"):
    global tournament
    global participants
    global matches
    global names

    USER = "haydunce" 
    KEY = "yCYu1uKVX10iNrRh5vJfy48ReZC2iQ0Kchi4xzMs"

    user = await challonge.get_user(USER, KEY)
    tournament = await user.get_tournament(url = tournament_name, force_update=True)
    participants = await tournament.get_participants(force_update=True)
    matches = await tournament.get_matches(force_update=True)
    
    for p in participants:
        names.append(p.name.lower())

def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(handler(loop, event, context))
    
async def handler(loop, event, context):
    await login()
    global tournament
    print("Tourney state " + tournament.state)
    print(tournament.started_checking_in_at)
    
    if event['request']['type'] == "LaunchRequest":
        return await on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return await intent_router(event, context)

async def on_launch(event, context):
    return statement("easy bracket","I'll do my best to help you with your tournament")

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
    
    if intent == "RuleSets":
        return statement("rules","The current rules are as follows. Three stocks, Eight minute timer, no items and hazards off.")
    
    if intent == "EndMatch":
        global names
        winner = event['request']['intent']['slots']['player']['value']
        if winner.lower() in names:
            participant_id = await get_id_from_participant(winner)
            match = await get_next_match_from_participant_id(participant_id)
            await update_match(match.id, participant_id)
            return statement("tWin Statement", "Okay, so " + winner + " is now a winner")
        else:
            return statement("Not in Tourney", "That person is not in the tournament")
        

#Custom Intents Functions
#--------------------------------------------------
async def start_tournament():
    global tournament
    await tournament.start()
    await tournament.abort_check_in()
    return statement("Tournament Started","The tournament has started")

async def reset_tournament():
    global tournament
    await tournament.reset()
    return statement("Tournament Reset","The tournament has been reset")

async def get_num_participants():
    global participants
    return statement("Number of Participants","There are " + str(len(participants)) + " participants")

async def get_next_open_match():
    global tournament
    current_match = None

    for m in matches:
        if(m.state == "open"):
            current_match = m

    return current_match

async def next_open_match():
    current_match = await get_next_open_match()

    part1 = await tournament.get_participant(current_match.player1_id, force_update=True)
    part2 = await tournament.get_participant(current_match.player2_id, force_update=True)
    player1 = part1.name
    player2 = part2.name

    return statement("Next Match",("The next match is between " + player1 + " and " + player2))
    
async def get_next_match_from_participant_id(participant_id):
    global matches
    for m in matches:
        if (m.player1_id == participant_id or m.player2_id == participant_id):
            if m.state == 'open':
                return m
    return None

#attempts to set the completed score/outcome
async def update_match(match_id, winner_id, scores = "0-0"):
    global tournament
    winner = await tournament.get_participant(winner_id, force_update=True)
    match = await tournament.get_match(match_id, force_update=True)
    if match.state == 'open':
        await match.report_winner(winner, scores)
    
    return None

#sends an email alert to the tournament organizer
def send_alert():
    SENDER = "Easy Bracket <easy.bracket@gmail.com>"
    RECIPIENT = "haydnnitzsche@gmail.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "Potential Issue on Tournament Floor"
    BODY_TEXT = ("somehting on the tournament floor requires your attention.")
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>easy bracket notification</h1>
    <p>somehting on the tournament floor requires your attention.</p>
    </body>
    </html>
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return statement("report sent","your report has been sent")

#Helpers
#--------------------------------------------------

#returns null if not found
async def get_id_from_participant(name):
    global participants
    for p in (participants):
        if p.name == name:
            return p.id
    return None

#Built in Intents Functions
#--------------------------------------------------
def cancel_intent():
    return statement("cancel","You want to cancel")
def help_intent():
    return statement("help","You want help")
def stop_intent():
    return statement("stop","You want to stop")

#Builders
#--------------------------------------------------
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
    return card

#Methods for testing
def get_matches():
    global matches
    return matches
