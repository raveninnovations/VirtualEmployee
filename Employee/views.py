import re
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError

from django.shortcuts import render,redirect
from .models import register
# Create your views here.

def Register(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password1']
        conform = request.POST['password2']
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if register.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used')
            return redirect('register')
        if name.isdigit():
            messages.error(request, 'name cannot have numbers')
            return redirect('register')
        if regex.search(name):
            messages.error(request, 'name cannot have special characters')
            return redirect('register')
        try:
            v = validate_email(email)
            val_email = v["email"]
        except EmailNotValidError as e:
            messages.error(request, 'Invalid Email ID')
            return redirect('register')
        try:
            if password == conform:
                data = register(name=name,email=email,password=password)
                data.save()
        except:
            usr = register.objects.get(email=email)
            usr.delete()
            messages.error(request,"some error occured")
            return redirect('register')
        messages.success(request,"User added successfully")

    return render(request,'virtualmain_pages/form-register.html')