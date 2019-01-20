# Easy Bracket
Run Challonge brackets with Alexa. Created by @HaydnNitzsche, @Jmarkaba, and @JoseTeuttli for HackArziona2019.

## Project Inspiration
The members of our group are smash-aholics. We can't get enough of the game. Haydn runs tournaments at his house, Jose will regularly drive out to events and Jah plays as much as possible with his friends. One thing we realized from our expereince is that running a tournament can be hectic. Setting up rulesets, ensuring correct reporting of results, and trying to be in 100 places at once takes its toll on a person. Luckily, with easy bracket, you no longer have to be in 100 places at once, Alexa can do it for you. With our new skill a tournament organizer can set up rulesets, allow players to report scores directly to the bracket, and  be notified of issues immediately. Our goal is to remove the stress from being a TO and allow them to have as much fun as the people playing.

## Project Summary
Initial concept decided upon, we planned to use Java or Javascript as the backend, Alexa as frontend, and Challonge's bracket hosting for the database. We familiarized ourself with the Alexa developer console and read through the documentation. We also attended a talk on Javascript and got a decent idea of what to do but when discussing our plan with the Amazon mentors we realized that a better approach would be to just use Python instead of Java or Javascript. We watched some tutorials and read through documentation. Learned how to upload libraries to the Lambda function and make the Challonge library accesible. We were finally able to implement stage one which was just starting the tournament using Alexa. From there we worked on rolling out features that allowed for further administration of the bracket using Alexa. We ran into an issue where the package we were using to run our API was unable to perform scorekeeping actions on the bracket. Because of this we were forced to begin from scratch with a new package. This package was written utilizing async functions which led to difficulty with gathering output. After *hours* of work trying to resolve this issue, including great assistance from mentors and even contacting the author of the package himself, we finally found that the package was dependent on a deprecated version of another package. This resolved we were back on track but
