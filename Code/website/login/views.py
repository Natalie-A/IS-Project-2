from django.shortcuts import render
import mysql.connector as sql

# Create your views here.
def loginaction(request):
    
    return render(request,'login_page.html')
