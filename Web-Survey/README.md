How do you build an online survey WITHOUT platforms like Google Forms, SurveyMonkey, Decipher, Confirmit, CMix[...]? Here's one of the closest to the roots of Python ways: 
Flask for the backend, Bootstrap for the frontend and SQLite for the database. It all began as a simple practice exercise for OOP and working with XML and afterwards I have
extended this to a fullstack project with respective backend, frontend and database engine included (and a pinch of data engineering/architecture included. Just a pinch...). 
And all of this - to show a different perspective of how my everyday work could look like. The survey is quite small, the questionnaire can be read in **qre.xml** and consists of 
one numeric, one single choice, one multiple choice, one open ended and one NPS-wannabe (the scale is 1-10 instead of 0-10) question - the idea is to serve as proof-of-concept 
instead of programming extremely complex survey. 
  1. Concept
     1.1. Program a survey in the most pythonic way possible - as most Python users know every goal can be achieved in more than one way. There are many other libraries that can be
     used for that purpose, Flask is just my way of doing so.
     1.2. Data validation can be done entirely on Python.
     1.3. Data validation can be done on two layers:
       1.3.1. Backend layer - this is the point where respondent's data was just collected from the web form BUT was not yet recorded to the database. On this layer I am using
       raw Python and I have developed two simple functions **(lib/validate.py)** changing data status from "valid" to "invalid" if inconcistencies appear. And in case record data
       becomes invalid - the record is rejected, otherwise respondent's data are written to db.
       1.3.2. Offline layer - on the first layer data are checked for each respondent separately. In this layer the data are checked in bulk for many/all respondents with
       direct connection to db. The **check_db_pandas.py** is supposed to be launched manually whenever data validation is needed.
  2. Tools - this actually an old project of mine I have built a couple of years ago, now I decided to revive it and re-factor some code with more up-to-date tools.
     2.1. Project structure and management - I have actually used **uv** to re-build the project, this is my new favorite pythonic thing. pyproject.toml stores all the details and
     versions needed for this project. Use "uv run main.py" to run the server and start the survey. 
     2.2. Backend - Flask. I prefer this framework when it comes to web development.
     2.3. Frontend - Bootstrap, if I remember well the exact version is 4.somehing.
     2.4. Database - This seems to be the best rdbms solution for online for several reasons, but mainly it is capable of having up to 32767 columns of data. Why is this important?
     In big data we have a lot of records in the database but relatively small number of columns - rarely more than 100. In market research field (yes, this is what
     I'm working) the situation is exactly the opposite - project data consists of relatively small amount of records (several hundred to several thousands in most cases,
     which is nothing compared to big data) and LOTS of columns, a project with less than 1000 columns is considered small. The largest project I've seen had 137 000 (+/-) columns
     and would not fit in a single table. However, such a big projects are rarity and most will fit below 32k columns. Why not another rdbms? Postgres for example has a limit of
     ~10000 columns (if I remember well) and would handle small to mid-sized projects, however, SQLite is far more flexible and easier to share/transfer, everything's in one file,
     etc. etc. etc.
     2.5. Data validation - as mentioned above I am using raw Python for the first layer of DV, and for the offline layer I am using the god-like pandas. I have tried another library
     called polars but the truth is in pandas... still. I have made some errors in the db on purpose to show how errors will be logged, all stored in **dv_reports/DP.log**.
     Use "uv run check_db_pandas.py" and you will get the log file.

**N.B.: .venv was created and maintained by uv when initiating the project and adding dependencies to it. I have made just an empty placeholder folder with the same name to maintain
project structure the same as on my PC.**
