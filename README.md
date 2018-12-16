# TimeManager

A website for managing timers during biological experiments. I made it just to get more experience with CSS, Javascript, Bootstrap, SQLalchemy, and managing a user base.
 Can be set up on linux by following these steps: 

1. Clone the repo and navigate to the top level folder.
2. Install dependencies by running `$pip install -r requirements.txt`
3. Run the setup file: `$bash setup.sh` to set up Redis
4. Setup up flask recaptcha w/ google recaptcha (https://www.youtube.com/watch?v=VrH0eH4nE-c)
5. Add public and private recaptcha key to config.py
6. Set the Flask app enviornment variable `$export FLASK_APP=timemanager.py`
7. Run the app by entering: `$flask run`


## Features

Landing page:

![picture alt](/readme_images/index.png)

Users can opt to get a "quick timer" by selecting "Quick Timer" on the center of the landing page or the Navbar. The 
timer itself was built on a CSS grid. The logic of the timer is written in Javascript. The user can select 1 of 4 unique
timer sounds that will play when the timer expires. The timer digits also shift from black to red font when the timer
expires.

![picture_alt](/readme_images/quick_timer.png)

TimeManager also supports a user base. After users register and login. They can choose to save multi-timer configurations
that have dedicated name and time settings. The users, as well as their configurations are saved in a SQL database.

![picture_alt](/readme_images/timer_setup.png)

A form with dynamically rendered input fields lets users setup up their timers.

![picture_alt](/readme_images/timer_form.png)

These timer configurations are then generated dynamically for the users.

![picture_alt](/readme_images/timer_array.png)

Users can always reload previously made timer configurations from the database by selecting "My Timers" from the navbar.

![picture_alt](/readme_images/my_timers.png)

## Extras

Timer Manager implements strategies to limit abuse by implementing Google reCaptcha in the registration form. The number
of requests clients make are stored using Redis and caps on requests are set with [Flask limiter](https://flask-limiter.readthedocs.io/en/stable/).
This is a common technique to throttle usage of web APIs that are vulnerable to abuse.






 