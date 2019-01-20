# Easy Bracket
Run Challonge brackets with Alexa

## Project Summary
Initial concept decided upon, planned to use Java or Javascript as the backend, Alexa as frontend, and Challonge's bracket hosting for the database. We familiarized ourself with the Alexa developer console and read through the documentation. We also attended a talk on Javascript and got a decent idea of what to do but when discussing our plan with the Amazon mentors we realized that a better approach would be to just use Python instead of Java or Javascript. We watched some tutorials and read through documentation. Learned how to upload libraries to the Lambda function and make the Challonge library accesible. We were finally able to implement stage one which was just starting the tournament using Alexa. From there we worked on rolling out features that allowed for further administration of the bracket using Alexa. We ran into an issue where the package we were using to run our API was unable to perform scorekeeping actions on the bracket. Because of this we were forced to begin from scratch with a new package. This package was written utilizing async functions which led to difficulty with gathering output.

# Running your own brackets
To run your own brackets, you will need an **AWS** account and an **Amazon Developer** account. TBC
