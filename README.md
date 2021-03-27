# Fencing virtual leaderboard

This is the source code for a responsive web application as a virtual leaderboard for Apex Fencing Academy to keep records of their fencers’
tournament results and highlight their top fencers, using Flask (Python) and MySQL. 
The tournament result submission form is user-friendly and accessible for fencers of all ages to input their tournament results.

## Technical structure:
The website is built using the Flask microframework and MySQL database for the backend, and simple HTML/CSS (Bootstrap) for the frontend. 
The Flask routings are available in `app.py`, while all the helper functions that deal with the database are in `funcs.py`.
The folder `templates` consists of all the html templates for the website pages, while `static` contains the styling in CSS as well as
`mobile-style.css` to make the website responsive. `db_making` contains the `sql` query ran to create the database.
