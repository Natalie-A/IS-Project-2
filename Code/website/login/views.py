from django.shortcuts import render

# Create your views here.
def loginaction(request):
    return render(request,'login_page.html')
