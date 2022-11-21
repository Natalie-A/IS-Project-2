from django.shortcuts import render
import mysql.connector as sql
from django.contrib import messages
from django.shortcuts import redirect
from decouple import config
import datetime

name = ''
email = ''
password = ''
emailAddress = ''
patientId = ''
fileName = ''
physicianId = ''
# Create your views here.


def welcome(req):
    return render(req, 'welcome.html')


def signaction(request):
    global name, email, password
    if request.method == "POST":
        m = sql.connect(host="localhost", user="root",
                        passwd=config("password"), database='project')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "full_name":
                name = value
            if key == "email":
                email = value
            if key == "password":
                password = value
        if len(password) == 0 or len(name) == 0 or len(email) == 0:
            messages.error(request, 'Please fill out all fields')
        elif len(password) < 8:
            messages.error(
                request, 'Password cannot be less than 8 characters')
        else:
            c = "insert into physician(fullName,emailAddress,password) Values('{}','{}','{}')".format(
                name, email, password)
            try:
                cursor.execute(c)
                m.commit()
                return redirect('login')
            except Exception:
                messages.error(request, 'Email already exists')

    return render(request, 'signup_page.html')


def loginaction(request):
    global email, password, emailAddress
    if request.method == "POST":
        m = sql.connect(host="localhost", user="root",
                        passwd=config("password"), database='project')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "email":
                email = value
            if key == "password":
                password = value
        request.session["emailAddress"] = email
        emailAddress = request.session["emailAddress"]
        c = "select * from physician where emailAddress='{}' and password='{}'".format(
            email, password)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if len(password) == 0 or len(email) == 0:
            messages.error(request, 'Please fill out all fields')
        elif t == ():
            messages.error(request, 'Invalid email or password')
        else:
            return redirect('input')
    return render(request, 'login_page.html')


def input(req):
    global patientId, fileName, physicianId
    if req.method == "POST":
        m = sql.connect(host="localhost", user="root",
                        passwd=config("password"), database='project')
        cursor = m.cursor()
        d = req.POST
        for key, value in d.items():
            if key == "patientId":
                patientId = value
            if key == "file":
                fileName = value
        ct = datetime.datetime.now()
        c = "select Id from physician where emailAddress ='{}'".format(
            emailAddress)
        cursor.execute(c)
        t = cursor.fetchall()
        for row in t:
            physicianId = row[0]
        if len(patientId)==0 or len(fileName)==0:
            messages.error(req,'Please fill out all fields')
        elif patientId.isnumeric() != True:
            messages.error(req,'Please enter a valid patientId')
        else:
            try:
                e = "insert into respiratory_sound_recordings(fileName,patientId,physicianId,dateOfUpload) values ('{}','{}','{}','{}')".format(
                    fileName, patientId, physicianId, ct)
                cursor.execute(e)
                m.commit()
            except Exception as e:
                messages.error(req, 'Please enter an existing patient Id')
    return render(req, 'input.html')


def logout(request):
    try:
        del request.session['emailAddress']
    except KeyError:
        pass
    return redirect('welcome')
