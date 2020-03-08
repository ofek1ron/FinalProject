"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from NewProject import app
from NewProject.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from NewProject.models.QueryFormStructure import QueryFormStructure 
from NewProject.models.QueryFormStructure import LoginFormStructure 
from NewProject.models.QueryFormStructure import UserRegistrationFormStructure

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from NewProject.models.Forms import ExpandForm
from NewProject.models.Forms import CollapseForm

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 



app.config['SECRET_KEY'] = 'The first argument to the field'

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact Me:',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About Me:',
        Me = 'static/Images/ImageOfMe.jpg',
        year=datetime.now().year,
    )

@app.route('/DataModel')
def DataModel():
    """Renders the about page."""
    return render_template(
        'DataModel.html',
        title='Data Model',
        year=datetime.now().year,
        message='My project is '
    )

@app.route('/NBAdraft' , methods = ['GET' , 'POST'])
def NBAdraft():
    form3 = ExpandForm()
    form4 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\NBA_Full_Draft_1947-2018.csv'))
    df = df[['Team', 'Player', 'College', 'Year', 'Pick']]
    raw_data_table = ''
 
    if (request.method == 'POST'):
        if (request.form['action'] == 'Expand' and form3.validate_on_submit()):
            raw_data_table = df.head(121).to_html(classes = 'table table-hover')      #I will present only the 120 first lines just to showcase some of the players picked in the NBA draft
        if (request.form['action'] == 'Collapse' and form4.validate_on_submit()):
            raw_data_table = ''
 
    return render_template(
    	'NBAdraft.html',
        title='NBA Draft:',
    	year=datetime.now().year,
        message='NBA draft details from 1947-2018 fields and data:',
        raw_data_table = raw_data_table,
    	form3 = form3,
    	form4 = form4
	)

@app.route('/GameDetails' , methods = ['GET' , 'POST'])
def GameDetails():
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\games_details.csv'))
    df = df[['TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_NAME', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']]
    raw_data_table = ''
 
    if (request.method == 'POST'):
        if (request.form['action'] == 'Expand' and form1.validate_on_submit()):
            raw_data_table = df.head(101).to_html(classes = 'table table-hover')      #I will present only the 100 first lines just to showcase some of the players playing in the NBA today
        if (request.form['action'] == 'Collapse' and form2.validate_on_submit()):
            raw_data_table = ''
 
    return render_template(
    	'GameDetails.html',
        title='Game Details:',
    	year=datetime.now().year,
        message='NBA game details from 2004-2020 fields and data:',
        raw_data_table = raw_data_table,
    	form1 = form1,
    	form2 = form2
	)

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thank You, You Will Register Now :) '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register A New User:',
        message='Please enter your new account details below',
        year=datetime.now().year,
        repository_name='Pandas',
        )



