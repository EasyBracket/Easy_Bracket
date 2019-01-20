#TODO
# - properly implement the built in intents
import json
import challonge
import boto3
from botocore.exceptions import ClientError
import smtplib

# Establish Challonge connection
#-------------------------------------------------------
USER = "haydunce" 
KEY = "yCYu1uKVX10iNrRh5vJfy48ReZC2iQ0Kchi4xzMs"
TOURNAMENT_NAME = "HackAZ"

challonge.set_credentials(USER, KEY)
tournament = challonge.tournaments.show(TOURNAMENT_NAME)
participants = challonge.participants.index(tournament["id"])
matches = challonge.matches.index(tournament["id"])

#Input handling
#-------------------------------------------------------
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
    
    if intent == "CurrentMatches":
        return current_matches()
    
    if intent == "EndMatch":
        return end_match()
        
    if intent == "ParticipantRank":
        return participant_rank()
    
    if intent == "NextMatch":
        return next_match()
    
    if intent == "NumberOfParticipants":
        return get_num_participants()
    
    if intent == "ResetTournament":
        return reset_tournament()
    
    if intent == "IncidentReport":
        return send_alert()

#Custom Intents Functions
#-------------------------------------------------------
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

def start_tournament():
    global tournament
    challonge.tournaments.start(tournament["id"])
    return statement("Tournament Started","The tournament has started",)

def reset_tournament():
    global tournament
    challonge.tournaments.reset(tournament['id'])
    return statement("Tournament Reset","The tournament has been reset")

def get_num_participants():
    global participants
    return statement("Number of Participants","There are " + str(len(participants)) + " participants")

def get_participant(id):
    global participants
    for p in (participants):
        if p['id'] == id:
            return p['name']
    return null

def next_match():
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

#Built in Intents Functions
#-------------------------------------------------------
def cancel_intent():
    return statement("","")
def help_intent():
    return statement("help","ask alexa to help you administer your tournament")
def stop_intent():
    return statement("","")

#Builders
#-------------------------------------------------------
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
