#---------------------------#
# Ofek Ron - Final Project  #
#---------------------------#
### ----------------------------------------------------------- ###
### ----- includes all software packages that are needed ------ ###
### ----------------------------------------------------------- ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from datetime import datetime
from NewProject import app
from NewProject.models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines

from NewProject.models.Forms import NBAForm
from NewProject.models.QueryFormStructure import LoginFormStructure 
from NewProject.models.QueryFormStructure import UserRegistrationFormStructure

from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

db_Functions = create_LocalDatabaseServiceRoutines() ## Directs to the local database

app.config['SECRET_KEY'] = 'The first argument to the field'


# =========================================== #
# === This is the route to the Home page: === #
# =========================================== #
@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


# ============================================== #
# === This is the route to the Contact page: === #
# ============================================== #
@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact Me:',
        year=datetime.now().year,
    )


# ============================================ #
# === This is the route to the About page: === #
# ============================================ #
@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About Me:',
        Me = 'static/Images/ImageOfMe.jpg',
        year=datetime.now().year,
    )


# =========================================== #
# === This is the route to the DataModel: === #
# =========================================== #
@app.route('/DataModel')
def DataModel():
    return render_template(
        'DataModel.html',
        title='Data Model',
        year=datetime.now().year,
        message='My project is '
    )


# ================================================ #
# === This is the route to the NBA Draft page: === #
# *This page was not used in the Query because the requirments for the final project were narrowed #
# ================================================ #
@app.route('/NBAdraft' , methods = ['GET' , 'POST'])
def NBAdraft():
    form3 = ExpandForm() ## Expands the database to be viewable by the user
    form4 = CollapseForm() ## Collapses the database back to being invisible
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\NBA_Full_Draft_1947-2018.csv')) ## Reads the csv NBA_Full_Draft_1947-2018 in the data section and sets it as the default df
    df = df[['Team', 'Player', 'College', 'Year', 'Pick']] ## Narrowing the original df to the columns needed for the page, In my case these 5 columns
    raw_data_table = '' ## Sets the database to hidden by deafult
 
    if (request.method == 'POST'):
        if (request.form['action'] == 'Expand' and form3.validate_on_submit()):
            raw_data_table = df.head(121).to_html(classes = 'table table-hover') ## When selecting the 'Expand' button, the first 121 values of the original df will be showed (I am showing the first 121 values just because I want to show a part of the dataset)
        if (request.form['action'] == 'Collapse' and form4.validate_on_submit()):
            raw_data_table = '' ## When selecting the 'Collapse', the df values are shown after selecting the 'Expand' button are hidden, back to the deafult stage
 
    return render_template(
    	'NBAdraft.html',
        title='NBA Draft:',
    	year=datetime.now().year,
        message='NBA draft details from 1947-2018 fields and data:',
        ## Saves the variable from the def to be used as a variable in the page html file:
        raw_data_table = raw_data_table,                                                  #
    	form3 = form3,                    #-----------------------------------------------#
    	form4 = form4                     #                                                                   
        #---------------------------------#
	)


# =================================================== #
# === This is the route to the Game Details page: === #
# =================================================== #
@app.route('/GameDetails' , methods = ['GET' , 'POST'])
def GameDetails():
    form1 = ExpandForm()
    form2 = CollapseForm() 
    df = pd.read_csv(path.join(path.dirname(__file__), 'static\\data\\games_details.csv')) ## reads the csv games_details in the data section and sets it as the default df
    df = df[['TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_NAME', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']] ## narrowing the original df to the columns needed for the page, In my case these columns
    raw_data_table = ''
 
    if (request.method == 'POST'): 
        if (request.form['action'] == 'Expand' and form1.validate_on_submit()):
            raw_data_table = df.head(101).to_html(classes = 'table table-hover') ## When selecting the 'Expand' button, the first 101 values of the original df will be showed (I am showing the first 101 values just because I want to show a part of the dataset)
        if (request.form['action'] == 'Collapse' and form2.validate_on_submit()):
            raw_data_table = '' ## When selecting the 'Collapse', the df values are shown after selecting the 'Expand' button are hidden, back to the deafult stage
 
    return render_template(
    	'GameDetails.html',
        title='Game Details:',
    	year=datetime.now().year,
        message='NBA game details from 2004-2020 fields and data:',
        raw_data_table = raw_data_table,
    	form1 = form1,
    	form2 = form2
	)


# ============================================ #
# === This is the route to the Login page: === #
# ============================================ #
@app.route('/Login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)
    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)): ## Searches in the users.csv If the username and password and valid to be used  
            flash('Login approved!')
            return redirect('Query') ## If the login is approved, redirect to the Query page
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'Login.html', 
        form=form, 
        title='Login As Existing User',
        message='Please enter your existing account details.',
        year=datetime.now().year, # Saves the current year in the variable 'year'
        repository_name='Pandas', 
    )

# =============================================== #
# === This is the route to the Register page: === #
# =============================================== #
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""
            return redirect('Login') ## If register is approved, redirect to the Login page

            flash('Thank You, You Will Register Now :) '+ form.FirstName.data + " " + form.LastName.data )
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


# ============================================ #
# === This is the route to the Query page: === #
# ============================================ #
@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():

    print("Query")

    form1 = NBAForm()
    chart = "https://lakersdaily.com/wp-content/uploads/2019/10/USATSI_13555447-e1572029064664.jpg"
    height_case_1 = "100"
    width_case_1 = "400"

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/games_details.csv')) ## Reads the csv games_details in the data section and sets it as the default df

    l = df["PLAYER_NAME"].tolist() ## Makes a list of all the NBA player who have played at least 1 minute in the NBA since 2004 (based on the csv)
    s = set(l)
    l = list(s)
    l.sort() ## Sorts the list of players in an alphabetical order
    m = list(zip(l,l)) ## Makes It so the list is presented in doubles, which will be helpful for the query
    form1.player_a.choices = m ## Sets the whole player list as available choices in the form field "player_a"
    form1.player_b.choices = m ## Sets the whole player list as available choices in the form field "player_b"

    hl = df.columns.tolist() ## Makes a list of all the In-game stat (columns) used in the df

    ## Removing the unnecessary columns from the edited df (hl)
    hl.remove('GAME_ID')
    hl.remove('TEAM_ID')
    hl.remove('TEAM_ABBREVIATION')
    hl.remove('TEAM_CITY')
    hl.remove('PLAYER_ID')
    hl.remove('PLAYER_NAME')
    hl.remove('START_POSITION')
    hl.remove('COMMENT')
    hl.remove('MIN')

    g = list(zip(hl,hl)) ## Makes it so the list is presented in doubles, which will help with the syntax in forms.py
    form1.catagory.choices = g ## Sets the available choices in the category field in the form as the catagories in the dataframe, it's in doubles to have appropriate syntax for the forms.py file
     
    if request.method=='POST':
         backgroundimg = "https://usathoopshype.files.wordpress.com/2018/12/demar_derozan_phone1.jpg?w=1000&h=701"
         player_a = form1.player_a.data ## The next 4 lines set the user choices from the form as a variable
         player_b = form1.player_b.data ##
         catagory = form1.catagory.data ##
         kind = form1.kind.data ##
         height_case_1 = "300"
         width_case_1 = "750"

         df = df[(df["PLAYER_NAME"] == player_a) | (df["PLAYER_NAME"] == player_b)] ## Sets the new df that presents only single-game stat-lines over the whole career of the selected two NBA players
         df = df[["PLAYER_NAME", catagory, "GAME_ID"]] ## Minimizes the df to the three relevent columns (catagory = In-game stat)

         df1 = pd.read_csv(path.join(path.dirname(__file__), 'static/data/games.csv')) ## Reads the csv games in the data section and makes a new df called df1
         df1 = df1[["GAME_ID", "GAME_DATE_EST"]] ## Minimizes df1 to 2 columns
         df1 = df1.set_index('GAME_ID') 
         s = df1["GAME_DATE_EST"]
         d = dict(s) 
    
         df['date'] = df['GAME_ID']
         df['date'] = df['date'].apply(lambda x: d.get(x))    ## Reads every field used (based on user request) and return the data (based on the date) to the df
         df = df[['PLAYER_NAME', catagory, 'date']]
         df2 = df.loc[df['PLAYER_NAME'] == player_a] ## Creates a new df (df2) with all the stats of the chosen player a
         df3 = df.loc[df['PLAYER_NAME'] == player_b] ## Creates a new df (df2) with all the stats of the chosen player b
         df2 = df2.set_index('date') ## Sets the x label to the date, based on player a
         df3 = df3.set_index('date') ## Sets the x label to the date, based on player b

         df2.index = pd.to_datetime(df2.index) ## This line and the next one turn the dates in the dataframe into datetime units
         df3.index = pd.to_datetime(df3.index) ##

         ## Creating the plot based on user choices and sets x and y labels
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
        ## Saves the variable from the def to be used as a variable in the page html file:
        form1 = form1,                                                                    #
        chart = chart,                     #----------------------------------------------#                          
        height_case_1 = height_case_1 ,    #
        width_case_1 = width_case_1        #
        #----------------------------------#
        
        
        )

## Turns the graph into an image (indepth)
def plt_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String



