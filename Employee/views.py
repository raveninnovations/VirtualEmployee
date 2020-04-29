import re
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import (AddUserForm)
from .models import UserDetails
# Create your views here.


def adminDashboard(request):
    return render(request,"Admin_pages/dashboard.html")



def adduser(request):
    form = AddUserForm
    if request.method =='POST':
        firstname = request.POST['name']
        lastname = request.POST['name']
        userphone = request.POST['user_phone']
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password1']
        conform = request.POST['password2']
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('register')
        if firstname.isdigit():
            messages.error(request, 'Name cannot have numbers')
            return redirect('register')
        if regex.search(firstname):
            messages.error(request, 'Name cannot have special characters')
            return redirect('register')
        try:
            v = validate_email(email)
            val_email = v["email"]
        except EmailNotValidError as e:
            messages.error(request, 'Invalid Email ID')
            return redirect('register')
        if password != conform:
            messages.error(request,'Password mismatch')
            return redirect('register')

        try:
            User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
            u_id = User.objects.get(username=username)
            addusr = UserDetails(user_id=u_id,user_pass=password,user_phone=userphone)
            addusr.save()

        except:
            usr = User.objects.get(username=email)
            usr.delete()
            messages.error(request, 'Some error occured !')
            return redirect('register')
        messages.success(request, 'User Added!')
        return redirect('register')
    context ={
        'form':form
    }
    return render(request,'virtualmain_pages/registermain.html',context)

def userlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                print('Welcome admin')
                return redirect(adminDashboard)
            messages.success(request,'Successfully loggedin')
            return redirect('login')
        else:
            messages.error(request,'Fail')
            return redirect('login')

    return render(request,'virtualmain_pages/login.html')

def logout(request):
    auth.logout(request)
    return render(request,'Admin_pages/logout.html')

@login_required
def userdashboard(request):
    return render(request,'virtualmain_pages/dashboard.html')