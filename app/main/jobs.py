from flask import Flask, flash, render_template, request,redirect,session
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField,SelectField
from wtforms.validators import data_required, length,Email
from . import main

currentJob = None
# Defining class for Job data
class JobData(FlaskForm):
     title = StringField('Title', validators=[data_required(), length(min=5)])
     salary = StringField('Salary Range', validators=[data_required()])
     email = StringField('Email',validators=[data_required(),Email()])
     company = StringField('Company',validators=[data_required()])
     category = SelectField('Category', choices=[('1', 'IT'), ('2', 'Finance'), ('3', 'Banking')])
     description = StringField('Description',validators=[data_required(),length(min=50)])
     submit = SubmitField('Submit')

# Add job functionality goes here
@main.route("/addjob", methods=['GET', 'POST'])
def addjob():
    addjobform = JobData()
    if request.method == 'POST':
        #if form.validate_on_submit():
        data = {
            "title": addjobform.title.data,
            "salary": addjobform.salary.data,
            "company": addjobform.company.data,
            "category_id": addjobform.category.data,
            "email": addjobform.email.data,
            "description": addjobform.description.data,
            "created_by":session.get("userid")
        }
        # Send the POST request to the API endpoint
        response = requests.post('http://localhost:5001/create-job',headers = {'Authorization': session.get("access_token"),'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200 or response.status_code == 201:
            return redirect("/")
        else:
            return 'Error Submitting Job'
        #else:
         #   return render_template('signup.html',form=form)
    else:
        return render_template('addjob.html',form=addjobform)

# Retrieval of job listings functionality goes here

@main.route("/", methods=['GET'])
def joblisting():
    access_token=session.get('access_token')
    response = requests.get('http://localhost:5001/jobs',headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        joblist = response.json()
    return render_template("joblisting.html",joblist=joblist)

# Filter job listing functionality goes here

@main.route("/jobs/<filter_text>", methods=['GET'])
def filterjobs(filter_text):
    access_token=session.get('access_token')
    data = {
        "filter_text":filter_text
    }
    response = requests.get('http://localhost:5001/jobs/filter',headers = {'Authorization': session.get("access_token"),'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 201:
        joblist = response.json()
    return render_template("joblisting.html",joblist=joblist)

# View  job functionality goes here

@main.route("/job/<id>", methods=['GET'])
def getjob(id):
    access_token=session.get('access_token')
    response = requests.get('http://localhost:5001/job?job_id='+id,headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        job = response.json()
    return render_template("viewjob.html",job=job)

# Edit job functionality goes here

@main.route("/job/edit/<id>", methods=['GET'])
def editjob(id):
    access_token=session.get('access_token')
    savejobform = JobData()
    currentJob = None
    response = requests.get('http://localhost:5001/job?job_id='+id,headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        currentJob = response.json()
    return render_template("editjob.html",form=savejobform,job=currentJob)

# Delete job functionality goes here

@main.route("/job/delete/<id>", methods=['GET'])
def deletejob(id):
    response = requests.delete('http://localhost:5001/delete-job?job_id='+id,headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        flash("Job deleted successfully")
        return redirect("/")

# Save job functionality goes here

@main.route("/savejob/<id>", methods=['GET', 'POST'])
def savejob(id):
    savejobform = JobData()
    if request.method == 'POST':
        #if form.validate_on_submit():
        data = {
            "title": savejobform.title.data,
            "salary": savejobform.salary.data,
            "company": savejobform.company.data,
            "category": savejobform.category.data,
            "email": savejobform.email.data,
            "description": savejobform.description.data,
            "job_id":id
        }
        # Send the POST request to the API endpoint
        response = requests.patch('http://localhost:5001/edit-job',headers = {'Authorization': session.get("access_token"),'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200 or response.status_code == 201:
            flash('Joblisting updated !')
            return redirect("/")
        else:
            return 'Error Saving Job'
        #else:
         #   return render_template('signup.html',form=form)
    else:
        return render_template('editjob.html',form=savejobform,job=currentJob)
