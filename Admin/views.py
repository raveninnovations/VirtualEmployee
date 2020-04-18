from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import (login)
# Create your views here.

def Login(request):

    if request.method == 'POST':
        name = request.POST['name']
        passord = request.POST['pass']
        try:
            detail = login.objects.get(password=passord)
            if name == detail.name:
                print('Success')
                context ={
                    "name":name
                }
                return redirect('dashboard')

        except:
            print("Error")
            messages.error(request, 'Email or Password is incorrect')
            return redirect('login')

    return render(request,'Admin_pages/form-modern-login.html')


def dasboard(request):

    print('Dashboard')
    return render(request,'Admin_pages/dashboard.html')