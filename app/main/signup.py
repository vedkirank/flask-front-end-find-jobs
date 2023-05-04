from flask import Flask, flash, render_template, request,redirect,session
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField,BooleanField
from wtforms.validators import data_required, length,Email
from . import main


class SignUpData(FlaskForm):
     name = StringField('Name', validators=[data_required(), length(min=2)])
     age = StringField('Age', validators=[data_required()])
     email = StringField('Email',validators=[data_required(),Email()])
     address = StringField('Address')
     phone_number = StringField('Mobile Number', validators=[data_required(), length(min=10)])
     date_of_birth = StringField('DOB', validators=[data_required()])
     password = PasswordField('Password', validators=[data_required(),length(min=3, message="Min 3 Char")])
     is_manager = BooleanField('Are you a Hiring Manager?')
     submit = SubmitField('Submit')

@main.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpData()
    if request.method == 'POST':
        #if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "age": form.age.data,
            "mobile": form.phone_number.data,
            "date_of_birth": form.date_of_birth.data,
            "email": form.email.data,
            "password": form.password.data,
            "address":form.address.data
        }
        if form.is_manager.data:
            service_url = "http://localhost:5001/create-manager"
        else:
            service_url = "http://localhost:5001/create-user"
        # Send the POST request to the API endpoint
        response = requests.post(service_url,headers = {'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200 or response.status_code == 201:
            print("REQUEST SUBMITEDDDD")
            flash('Signup successful')
            return redirect('joblisting')
        else:
            return 'Error submitting form'
        #else:
         #   return render_template('signup.html',form=form)
    else:
        return render_template('signup.html',form=form)
