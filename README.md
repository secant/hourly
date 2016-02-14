# Pic-y Eats
A web app for food enthusiasts. Built with Flask, Microsoft Azure, Python, SQLite, HTML, CSS, JavaScript.
Check it out: http://pic-yeats.azurewebsites.net

*Built at TreeHacks 2016 at Stanford University*
http://devpost.com/software/pic-y-eats

**What it does**
Pic-y Eats (pronounced picky eats!) is a photo web app social media platform that generates a food-related theme of the day, then gives users a randomly selected 2 hour slot to upload photos which fit the theme. Users can browse the main feed to see photos that other users upload. Each upload is accompanied with a description, so people can add anything from family recipes to restaurant addresses!

We also implemented a form validation system that allows for users to register and log in smoothy.

**Inspiration**
Instagram and #food inundates us 24/7 with endless streams of acai bowls and chicken wings. We wanted to have the fun of looking at delicious foods without the nonstop updates (you could say we wanted to have our cake and eat it too), so we came up with a tall order for Pic-y Eats.

Check in to Pic-y Eats in the morning to see the Food of the Day and the time slot, then spend your day adventuring to snap a picture of the chosen delicacy. Come back again during the time slot, share, and see what others have posted! Share your love for food: upload/talk about your home-made baked cookies, or about the pasta at the new chic restaurant that opened on University Ave. You can see foods from different cultures, different cities, and different countries.

**How we built it**
We used Flask as our framework, SQLite as our database, and Microsoft Azure as our platform.

**Challenges we ran into**
Generating a time slot for daily uploads. To accommodate for the possibility of the web app being unexpectedly terminated, we generated a new time slot for the current day whenever the app is launched. But the time slot had to be reasonable (within 7am to 12pm) for the users' schedules; we couldn't just generate a random timedate instance. What if the app were launched at a time that was _ after _ the generated random slot? We eventually implemented a system to accurately generate time slots, update times when the slot for today has expired, and inform the user of their next available times to post!

Learning Flask and Azure Within 24 hours, we read our very first Flask tutorial, installed necessary files, built a Flask web app, then deployed to Azure! We haven't had much prior experience with HTTPS methods, and that was an interesting challenge as well.

**Accomplishments that we're proud of**
Implementing the user login process was much harder than it looks. We learned to use databases to manage user identities, streamline the process of registration, and accurately check passwords at login.

After login, it was a challenge figuring out how to keep track of the file after the user selects it, and then serve it back again. Because Flask was totally new to us, there were many nuances associated with it and SQLite that we encountered then conqeured.

**What we learned**
For everyone on our team, it's our first time using Flask and Azure! We learned to integrate HTML with Flask, set up directories for webapps, and deploy using Azure with SQLite.

**What's next for Pic-y Eats**
A more robust user login system, as well as the ability to view user profiles and see all the photos and user has posted. We could also crowdsource the theme-generating process, with the next day's theme chosen by popular vote. Timezone support would be added as well, because currently the time depends on the Azure servers hosting our webapp. Other features include image compression, ability to tag other in your posts, and ability to edit photos before posting.

