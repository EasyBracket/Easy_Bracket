<p align="center"><img src ="https://github.com/HaydnNitzsche/Easy_Bracket/blob/master/logos/EasyBracketSmall.png?raw=true" /></p>

# Easy Bracket
Run Challonge brackets with Alexa. Created by @HaydnNitzsche, @Jmarkaba, and @JoseTeuttli for HackArziona2019. Works in Python 3.6.

## Project Inspiration
The members of our group are smash-aholics. We can't get enough of the game. Haydn runs tournaments at his house, Jose will regularly drive out to events, and Jah plays as much as possible with his friends. One thing we realized from our experience is that running a tournament can be hectic. Setting up rulesets, ensuring correct reporting of results, and trying to be in 100 places at once takes its toll on an individual. Luckily, with Easy Bracket you no longer have to be in 100 places at once, Alexa can do it for you. With our new skill a tournament organizer can set up rulesets, allow players to report scores directly to the bracket, and be notified of issues immediately. The goal is to remove the stress of being a tournament organizer and allow tournament organizers to have as much fun as the attendees.

## Project Summary
Utilizes the [achallonge]{https://github.com/fp12/achallonge} library to access [Challonge's](https://challonge.com) API. Passes through Alexa commands to the API and returns that information to Alexa. Easy bracket can:
 - Start a tournament
 - Reset a tournament
 - Report scores
 - Provide information on the match schedule
 - Provide rules information
 - Notify tournament organizers of issues via e-mail

## Dependencies
- `achallonge`
- `asyncio`
- `boto3`
- `json`

## How to run this code yourself
To set up the Alexa end of things, sign into the [Alexa Developers Console](https://developer.amazon.com/alexa/console/ask). Create a new skill and click into the JSON editor. Here you can either copy + paste the code from [interaction_model.json](https://github.com/HaydnNitzsche/Easy_Bracket/blob/master/interaction_model.json) or upload the file itself. While you are in the Alexa Developers Console, click into the endpoints section and copy the Skill ID.

Next you will need to sign into AWS. From there search Lambda and from the dashboard click "create function". Once you are within the function, select "Alexa Skills Kit" from the list of triggers on the left in the designer section. You will need to paste your Skill ID into the configuration window. While you are on this page, make sure that your runtime is Python 3.6. Additionally, copy the ARN code in the top right of your screen.

Return to the alexa skills page and the endpoint subsection. In the default region section, paste your ARN. Make sure you save your endpoints. At this point, your Lambda function and the skill are connected.

To add the code that runs the API requests, follow the instructions in [this article](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html#python-package-dependencies), particularly under the heading "WWith Additional Dependencies".

Should everything be done correctly, you should be able to run the skill in the test window of the Alexa Developers Console.

## External Links
- [Demo Challonge Bracket](https://challonge.com/HackAZ)
- [Alexa Simulator](https://echosim.io/welcome)
- [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
- [AWS Console](https://console.aws.amazon.com/console/home)
