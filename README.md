# Cloning repository

First clone the repository from Github and switch to the new directory:

    $ git clone
    $ cd leads-backend


# Setting up the environment

Rename conceptor/.env.example to .env:
    $ cd conceptor
    $ mv .env.example .env
    $ cd ../

Set proper values to environment variables


# Getting Started

Create and Activate the virtualenv for your project.

    $ python -m venv venv
    $ source venv/bin/activate

Install project dependencies:

    $ pip install -r requirements.txt

Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver


# Creating an admin user

First we’ll need to create a user who can login to the admin site. Run the following command:

    $ python manage.py createsuperuser

Username: admin<br/>
Email address: admin@example.com<br/>
Password: *****<br/>
Password (again): *****<br/>


# Creating a decision tree question as admin

Enter admin site (hostname_or_ipaddress/admin) using admin user<br/>
Click Questions under API section<br/>
Click ADD QUESTION<br/>
In Data, insert content from decision_tree_data.json (root directory)<br/>
Click SAVE<br/>


# Adding a synergy mission from dataset for program x output sample

Enter admin site (hostname_or_ipaddress/admin) using admin user<br/>
Click Synergy missions under API section<br/>
Click ADD SYNERGY MISSION<br/>
Insert content from example_5_alg_output.csv to corresponding fields (root directory)<br/>
Click SAVE<br/>


# Importing synergy mission (and other dataset) Data via Django Admin

Enter admin site (hostname_or_ipaddress/admin) using admin user<br/>
Click Synergy missions under API section<br/>
Click Upload a csv file<br/>
Click Choose File, and choose a csv file<br/>
Click Upload File<br/>
