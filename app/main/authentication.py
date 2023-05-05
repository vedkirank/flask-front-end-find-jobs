from flask import Flask, flash, render_template, request,redirect,session
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField,BooleanField
from . import main
from wtforms.validators import data_required, length,Email

# A class for Login data
class LoginData(FlaskForm):
    email = StringField('Email', validators=[data_required(), Email()])
    password = PasswordField('Password', validators=[data_required()])
    is_manager = BooleanField('Are you a Hiring Manager?')
    submit = SubmitField('Submit')

# Login functionality goes here
@main.route("/login", methods=['GET', 'POST'])
def login():
    loginform = LoginData()
    #if loginform.validate_on_submit():
    data = {
            "email":loginform.email.data,
            "password":loginform.password.data,
            "is_manager":loginform.is_manager.data
            }
    response = requests.get('http://localhost:5001/login',headers = {'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 201:
        if response.json()['is_manager']:
            session['access_token'] = response.json()['access_token']
            session['username'] = response.json()['manager']['name']
            session['userid'] = response.json()['manager']['id']
            session['is_manager'] = True
            flash("Login successful")        
            return redirect("/")
        else:
            session['access_token'] = response.json()['access_token']
            session['username'] = response.json()['user']['name']
            session['userid'] = response.json()['user']['id']
            session['is_manager'] = False
            flash("Login successful")        
            return redirect("/")
    else:
        return render_template('login.html',form=loginform)
    #else:
    #    return render_template('login.html',form=loginform)

# Logout functionality goes here

@main.route("/logout")
def logout():
    session.clear()
    flash('Logout Successful !')
    return redirect("/")

