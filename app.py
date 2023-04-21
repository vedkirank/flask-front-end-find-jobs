from flask import Flask, render_template, request,redirect,session
import requests
import json
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField,validators,SelectField,TextAreaField,BooleanField
from wtforms.validators import data_required, length,Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jobseekersappsecretkey'
currentJob = None
class LoginData(FlaskForm):
    email = StringField('Email', validators=[data_required(), Email()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Submit')

class SignUpData(FlaskForm):
     name = StringField('Name', validators=[data_required(), length(min=2)])
     age = StringField('Age', validators=[data_required()])
     email = StringField('Email',validators=[data_required(),Email()])
     address = StringField('Address')
     phone_number = StringField('Mobile Number', validators=[data_required(), length(min=10)])
     date_of_birth = StringField('DOB', validators=[data_required()])
     password = PasswordField('Password', validators=[data_required(),length(min=3, message="Min 3 Char")])
     is_manager = BooleanField('Are you a Manager?')
     submit = SubmitField('Submit')

class JobData(FlaskForm):
     title = StringField('Title', validators=[data_required(), length(min=5)])
     salary = StringField('Salary Range', validators=[data_required()])
     email = StringField('Email',validators=[data_required(),Email()])
     company = StringField('Company',validators=[data_required()])
     category = SelectField('Category', choices=[('1', 'IT'), ('2', 'Finance'), ('3', 'Banking')])
     #description = TextAreaField('Description',render_kw={"rows": 10}, validators=[data_required(),length(min=100, message="Min 100 Characters")])
     description = StringField('Description',validators=[data_required(),length(min=50)])
     submit = SubmitField('Submit')

@app.route("/login", methods=['GET', 'POST'])
def login():
    loginform = LoginData()
    #if loginform.validate_on_submit():
    data = {
            "email":loginform.email.data,
            "password":loginform.password.data,
            "is_manager":True
            }
    print("data:::",data)
    response = requests.get('http://localhost:5001/login',headers = {'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 201:
        print("LOGIN REQUEST SUCCESSFULL")
        print(response.json())
        session['access_token'] = response.json()['access_token']
        session['username'] = response.json()['manager']['name']
        session['userid'] = response.json()['manager']['id']
        session['is_manager'] = True
        print(response.json()['access_token'])
        return redirect("/joblisting")
    else:
        return render_template('login.html',form=loginform)
    #else:
    #    return render_template('login.html',form=loginform)


         
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpData()
    if request.method == 'POST':
        print("POSTING")
        #if form.validate_on_submit():
        print("VALIDATION DONE")
        data = {
            "name": form.name.data,
            "age": form.age.data,
            "mobile": form.phone_number.data,
            "date_of_birth": form.date_of_birth.data,
            "email": form.email.data,
            "password": form.password.data,
            "address":"106 Woodland street"
        }
        # Send the POST request to the API endpoint
        response = requests.post('http://localhost:5001/signup',headers = {'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200 or response.status_code == 201:
            print("REQUEST SUBMITEDDDD")
            return 'Form submitted successfully'
        else:
            return 'Error submitting form'
        #else:
         #   return render_template('signup.html',form=form)
    else:
        return render_template('signup.html',form=form)

@app.route("/addjob", methods=['GET', 'POST'])
def addjob():
    addjobform = JobData()
    if request.method == 'POST':
        print("Adding Job")
        #if form.validate_on_submit():
        print("VALIDATION DONE")
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
        print("$$$$$$$$$$$$")
        print(data)
        response = requests.post('http://localhost:5001/create-job',headers = {'Authorization': session.get("access_token"),'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200 or response.status_code == 201:
            print("CREATE JOB REQUEST SUBMITEDDDD")
            return redirect("/joblisting")
        else:
            return 'Error Submitting Job'
        #else:
         #   return render_template('signup.html',form=form)
    else:
        return render_template('addjob.html',form=addjobform)

@app.route("/joblisting", methods=['GET'])
def joblisting():
    access_token=session.get('access_token')
    print("ACCESS TOKEN:::",session.get("access_token"))
    response = requests.get('http://localhost:5001/jobs',headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        print("REQUEST SUBMITEDDDD")
        joblist = response.json()
        print("JOBLIST-->",joblist)
    return render_template("joblisting.html",joblist=joblist)

@app.route("/jobs/<filter_text>", methods=['GET'])
def filterJobs(filter_text):
    access_token=session.get('access_token')
    print("ACCESS TOKEN:::",session.get("access_token"))
    data = {
        "filter_text":filter_text
    }
    print("data::",data)
    response = requests.get('http://localhost:5001/jobs/filter',headers = {'Authorization': session.get("access_token"),'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 201:
        print("REQUEST SUBMITEDDDD")
        joblist = response.json()
        print("JOBLIST-->",joblist)
    return render_template("joblisting.html",joblist=joblist)


@app.route("/job/<id>", methods=['GET'])
def getJob(id):
    access_token=session.get('access_token')
    print("ACCESS TOKEN:::",session.get("access_token"))
    response = requests.get('http://localhost:5001/job?job_id='+id,headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        print("REQUEST SUBMITEDDDD")
        job = response.json()
        print("JOBLIST-->",job)
    return render_template("viewjob.html",job=job)

@app.route("/job/edit/<id>", methods=['GET'])
def editJob(id):
    access_token=session.get('access_token')
    savejobform = JobData()
    currentJob = None
    print("ACCESS TOKEN:::",session.get("access_token"))
    response = requests.get('http://localhost:5001/job?job_id='+id,headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        print("REQUEST SUBMITEDDDD")
        currentJob = response.json()
    return render_template("editjob.html",form=savejobform,job=currentJob)

@app.route("/job/delete/<id>", methods=['GET'])
def deleteJob(id):
    print("ACCESS TOKEN:::",session.get("access_token"))
    response = requests.delete('http://localhost:5001/delete-job?job_id='+id,headers = {'Authorization': session.get("access_token")})
    if response.status_code == 200 or response.status_code == 201:
        print("DELETE REQUEST SUBMITEDDDD")
        return redirect("/joblisting")


@app.route("/savejob/<id>", methods=['GET', 'POST'])
def savejob(id):
    savejobform = JobData()
    if request.method == 'POST':
        print("Saving Job")
        #if form.validate_on_submit():
        print("VALIDATION DONE")
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
        print("$$$$$$$$$$$$")
        print(data)
        response = requests.patch('http://localhost:5001/edit-job',headers = {'Authorization': session.get("access_token"),'Content-Type': 'application/json'}, data=json.dumps(data))
        if response.status_code == 200 or response.status_code == 201:
            print("CREATE JOB REQUEST SUBMITEDDDD")
            return redirect("/joblisting")
        else:
            return 'Error Saving Job'
        #else:
         #   return render_template('signup.html',form=form)
    else:
        return render_template('editjob.html',form=savejobform,job=currentJob)
    



@app.route("/logout")
def logout():
    session.clear()
    print("TOKEN AFTER CLEARING",session.get("access_token"))
    return redirect("/joblisting")