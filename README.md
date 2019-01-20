# Easy Bracket
Run Challonge brackets with Alexa. Created by @HaydnNitzsche, @Jmarkaba, and @JoseTeuttli for HackArziona2019.

## Project Inspiration
The members of our group are smash-aholics. We can't get enough of the game. Haydn runs tournaments at his house, Jose will regularly drive out to events, and Jah plays as much as possible with his friends. One thing we realized from our experience is that running a tournament can be hectic. Setting up rulesets, ensuring correct reporting of results, and trying to be in 100 places at once takes its toll on an individual. Luckily, with Easy Bracket you no longer have to be in 100 places at once, Alexa can do it for you. With our new skill a tournament organizer can set up rulesets, allow players to report scores directly to the bracket, and be notified of issues immediately. The goal is to remove the stress of being a tournament organizer and allow tournament organizers to have as much fun as the attendees.

## Project Summary
Initial concept decided upon, we planned to use Java or Javascript as the backend, Alexa as frontend, and Challonge's bracket hosting for the database. We familiarized ourselves with the Alexa developer console and read through the documentation. We also attended a talk on Javascript and got a decent idea of what to do, however when discussing our plan with the Amazon mentors we realized that a better approach was available. That is to use Python instead of Java or Javascript. We watched some tutorials and read through documentation. Learned how to upload libraries to the Lambda function and make the Challonge library accessible.

Next we were able to implement stage one which was just starting the tournament using Alexa. Stage two was rolling out necessary features that allowed for administration of the bracket using Alexa such as starting matches, reporting matches, and finalizing the tournament. We ran into an issue where pichal, the package we were using to run our API, was unable to perform scorekeeping actions on the bracket. This forced us to begin from scratch with a new package, achallonge. This package was written utilizing async functions which led to difficulty with gathering output. After *hours* of work trying to resolve this issue, including substantial assistance from mentors, and even contacting the author of the package himself, we finally found that the package was dependent on a deprecated version of another package. We at first fixed this by using the deprecated package but worked with the package's author to update the package's files.

We needed to resolve some issues with running asynchronous functions in Lambda but were able to work around it using a loop and some weird Python technicalities. The final hurdle was figuring out some of the more esoteric aspects of Challonge's API but we got it done.

## External Links
- [Challonge Bracket](https://challonge.com/HackAZ/participants)
- [Alexa Simulator](https://echosim.io/welcome)
