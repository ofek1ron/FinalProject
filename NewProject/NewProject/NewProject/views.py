"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from NewProject import app
from NewProject.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from NewProject.models.Forms import NBAForm
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

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)
    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('Query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'Login.html', 
        form=form, 
        title='Login As Existing User',
        message='Please enter your existing account details.',
        year=datetime.now().year,
        repository_name='Pandas',
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
            flash('Error: aUser with this Username already exist! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form,
        title='Register A New User:',
        message='Please enter your new account details below.',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():

    print("Query")

    form1 = NBAForm()
    chart = "https://lakersdaily.com/wp-content/uploads/2019/10/USATSI_13555447-e1572029064664.jpg"
    height_case_1 = "100"
    width_case_1 = "400"

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/games_details.csv'))

    l = df["PLAYER_NAME"].tolist()
    s = set(l)
    l = list(s)
    l.sort()
    m = list(zip(l,l))
    form1.player_a.choices = m
    form1.player_b.choices = m

    hl = df.columns.tolist()
    hl.remove('GAME_ID')
    hl.remove('TEAM_ID')
    hl.remove('TEAM_ABBREVIATION')
    hl.remove('TEAM_CITY')
    hl.remove('PLAYER_ID')
    hl.remove('PLAYER_NAME')
    hl.remove('START_POSITION')
    hl.remove('COMMENT')
    g = list(zip(hl,hl))

    form1.catagory.choices = g
     
    if request.method=='POST':
         backgroundimg = "https://usathoopshype.files.wordpress.com/2018/12/demar_derozan_phone1.jpg?w=1000&h=701"
         player_a = form1.player_a.data
         player_b = form1.player_b.data
         catagory = form1.catagory.data
         kind = form1.kind.data
         height_case_1 = "300"
         width_case_1 = "750"

         print(player_a)
         print(player_b)
         print(catagory)
         print(kind)

         df = df[(df["PLAYER_NAME"] == player_a) | (df["PLAYER_NAME"] == player_b)]
         df = df[["PLAYER_NAME", catagory, "GAME_ID"]]

         df1 = pd.read_csv(path.join(path.dirname(__file__), 'static/data/games.csv'))
         df1 = df1[["GAME_ID", "GAME_DATE_EST"]]
         df1 = df1.set_index('GAME_ID')
         s = df1["GAME_DATE_EST"]

  
         d = dict(s) 
    

         df['date'] = df['GAME_ID']

         df['date'] = df['date'].apply(lambda x: d.get(x))

         df = df[['PLAYER_NAME', catagory, 'date']]

         df2 = df.loc[df['PLAYER_NAME'] == player_a]

         df3 = df.loc[df['PLAYER_NAME'] == player_b]

         df2 = df2.set_index('date')
         df3 = df3.set_index('date')

         df2.index = pd.to_datetime(df2.index)
         df3.index = pd.to_datetime(df3.index)

         #df2 = df2[start_date:end_date]
         #df3 = df3[start_date:end_date]



         fig1 = plt.figure()
         axx = fig1.add_subplot(111)
         df2[catagory].plot(legend = True, ax = axx)
         df3[catagory].plot(secondary_y = True, legend = True, ax = axx)
         axx.set_ylabel(player_a)
         axx.right_ax.set_ylabel(player_b)

         chart=plt_to_img(fig1) # Turns the graph into an image
    
   
    

    return render_template(
        'query.html',
        title = 'NBA Player Comparison:',
        message = 'Please select 2 NBA players*, then select a category** (in-game stat), then select the chart kind. When you are done please click Compare.',
        form1 = form1,
        chart = chart,
        height_case_1 = height_case_1 ,
        width_case_1 = width_case_1 
        
        
        )
def plt_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String



