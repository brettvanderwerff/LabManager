# TimeManager

WIP Website for managing time during biological experiments. Made to practice CSS, Javascript and SQL. When
complete, the website will allow users to log in and save customized arrays of timers for experiments. Is not ready 
for deployment but does have some unpolished functionality now and can be set up on linux by following these steps: 

1. Clone the repo and navigate to the top level folder.
2. Install dependencies by running `$pip install requirements.txt`
3. Run the setup file: `$bash setup.sh` to set up Redis
4. Setup up flask recaptcha w/ google recaptcha (https://www.youtube.com/watch?v=VrH0eH4nE-c)
5. Set the Flask app enviornment variable `$export FLASK_APP=timemanager.py`
6. Run the app by entering: `$flask run`