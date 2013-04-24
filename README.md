penn_tickets_app
================
To launch database use
from app import db
db.create_all()

Working on our Web App was a lot of fun, and we learned quite a bit about how to use python in this process, as well as quite a bit of CSS styling. In terms of our proposal, we accomplished the goals that we had originally thought feasible. With that being said, there is still plenty of room for improval in this project. And one of us plans to continue working on it over the summer in the hopes of turning it into a real service here at Penn.

In terms of the features we accomplished, we built login functionality from scratch for both students and groups. We built both student and group models as well as an event model which served as the crux of the app. We then created functionality for groups to make new events, and then view some rudimentary information about their event, as well as give them access to a printable list of attendees. The group's landing page is basically a list of all their previous and upcoming events, and they can click on them for more information. We realized that we did not have ample time to implement a third party api for payments, so went with this more "hack-ish" approach. On the student side, students can view a list of all the upcoming events, and then click on them to find out more information. Students also have th ability to "purchase" a ticket. What this does is add to the event model an attendee in its field, which can then be reported back to the group. 

Reflecting back on our work, we realized that in the end a large portion of our time became caught up in working with html and css, as opposed to issues with coding in python. The python component of the project was straight-forward, as it mainly handles the functionality of routing users to the various appropriate pages, css and html however could get annoying at times. Another new tool we had to learn was sqlalchemy, the database we chose to store all of event, group, and student models. While intimidating at first, this was quite easy to make use of after some initial reading. 

In summary, we enjoyed working on our app, and look forward to continuing to make it better even after this clsas is over. While it may not have been very heavy on python, it was still great to be able to use a new language to cook up a web app from scratch.
