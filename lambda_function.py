import json
import challonge
import asyncio

tournament = None
participants = []
matches = None

#Startup
#--------------------------------------------------
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

async def lambda_handler(event, context):
    await login()
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)

def on_launch(event, context):
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
    
    if intent == "EndMatch":
        
        return await update_match(get_next_match().id, )

#Custom Intents Functions
#--------------------------------------------------
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

#sends an email alert to the tournament organizer
def send_alert():
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "haydn nitzsche <hnitzsch@asu.edu>"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "haydnnitzsche@gmail.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"
    
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # The subject line for the email.
    SUBJECT = "Potential Issue on Tournament Floor"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("There is an issue being reported on the floor."
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>easy bracket notification</h1>
    <p>There is an issue being reported on the floor.</p>
    </body>
    </html>
                """            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
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

def rules():
    return statement("rules","The current rules are as follows: 3 stocks, 8 minute timer, no items and hazards off.")

#Helpers
#--------------------------------------------------

#returns null if not found
async def get_id_from_participant(name):
    global participants
    for p in (participants):
        print(p.name)
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

#Methods for testing
def get_matches():
    global matches
    return matches
