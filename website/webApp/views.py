from django.shortcuts import render
import mysql.connector as sql
from django.contrib import messages
from django.shortcuts import redirect
from decouple import config

name = ''
email = ''
password = ''
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
        if len(password)<8:
            messages.error(request,'Password cannot be less than 8 characters')
        else:
            c = "insert into physician(fullName,emailAddress,password) Values('{}','{}','{}')".format(
                name, email, password)
            try:
                cursor.execute(c)
                m.commit()
                return redirect('login')
            except Exception:
                messages.error(request,'Email already exists')

    return render(request, 'signup_page.html')


def loginaction(request):
    global email, password
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

        c = "select * from physician where emailAddress='{}' and password='{}'".format(
            email,password)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if t == ():
            messages.error(request, 'Invalid email or password')
        else:
            return redirect('input')
    return render(request, 'login_page.html')


def input(req):
    return render(req, 'input.html')
