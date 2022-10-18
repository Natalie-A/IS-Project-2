from django.shortcuts import render
import mysql.connector as sql
fullName = ''
emailAddress = ''
password = ''

# Create your views here.
def signaction(request):
    global fullName,emailAddress,password
    if request.method == "POST":
        m = sql.connect(host="localhost", user = "root", passwd="tallieNat7", database = "project")
        cursor = m.cursor()
        d= request.POST
        for key,value in d.items():
            if key =="full_name":
                fullName = value
            if key == "email":
                emailAddress = value
            if key == "password":
                password = value
            
        c="insert into physician(fullName,emailAddress,password) values('{}','{}','{}')".format(fullName,emailAddress,password)
        cursor.execute(c)
        m.commit()
    
    return render(request,'signup_page.html')
