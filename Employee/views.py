import re
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import (AddUserForm, EditUserProfileForm)
from .models import UserDetails, UserProfile
# Create your views here.
# ADMIN SECTION

@login_required
def adminDashboard(request):
    return render(request,"Admin_pages/dashboard.html")

@login_required
def adminCourses(request):
    return render(request,'Admin_pages/courses.html')

@login_required
def adminAddcourse(request):
    return render(request,'Admin_pages/add-course.html')

@login_required
def adminProjects(request):
    return render(request,'Admin_pages/projects.html')

@login_required
def adminRolecreation(request):
    return render(request,'Admin_pages/role-creation.html')


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
            return redirect(userdashboard)
            messages.success(request,'Successfully loggedin')
            return redirect('login')
        else:
            messages.error(request,'Fail')
            return redirect('login')

    return render(request,'virtualmain_pages/login.html')


def logout(request):
    auth.logout(request)
    return render(request,'Admin_pages/logout.html')

# USER SECTION

@login_required
def userdashboard(request):

    return render(request,'virtualmain_pages/dashboard.html')


@login_required
def userprofile(request):
    return render(request,'virtualmain_pages/user-profile.html')



@login_required
def userEdit(request):

    EditProfile = EditUserProfileForm

    if request.method == 'POST':
        user_profile_image   = request.POST['user_profile_image']
        first_name           = request.POST['firstname']
        last_name            = request.POST['lastname']
        username             = request.POST['email'] 
        gender               = request.POST['gender']
        email             = request.POST['email']
        contact_no           = request.POST['phone']
        address              = request.POST['address']

        degree               = request.POST['degree']
        specialisation       = request.POST['specialisation']
        current_year         = request.POST['current_year']
        institution_name     = request.POST['institution_name']
        institution_address  = request.POST['institution_address']
        career_category      = request.POST['career_category']
        career_specification = request.POST['career_specification']

        try:
            u_id = User.objects.get(username=username)
            edituser = UserProfile(user_id=u_id,user_profile=user_profile_image,gender=gender,contact_no=contact_no,address=address,degree=degree,specialisation=specialisation,institution_name=institution_name,institution_address=institution_address,career_category=career_category,career_specification=career_specification)
            edituser.save()

        except:
            usr = User.objects.get(username=email)
            usr.delete()
            messages.error(request, 'Some error occured !')
            return redirect('user-profile-edit')
        messages.success(request, 'User profile edited Successfully!')
        return redirect('user-profile-edit')

    context ={

        'form':EditProfile
    }


    return render(request,'virtualmain_pages/user-profile-edit.html',context)



def userProject(request):
    return render(request,'virtualmain_pages/user-project.html')

# CSM MODULE SECTION

def csmDashboard(request):
    return render(request,'csm_pages/csm_dashboard.html')

def csmAddCourse(request):
    return render(request,'csm_pages/csm_add_course.html')

# TL MODULE SECTION

def tlDashboard(request):
    return render(request,'TL_Pages/tl_dashboard.html')

def tlProjectDetails(request):
    return render(request,'TL_Pages/tl_project_details.html')

# PROJECT MODULE SECTION

def projectManager(request):
    return render(request,'ProjectModule_Pages/Project_manager.html')

def projectDashboard(request):
    return render(request,'ProjectModule_Pages/Project_dashboard.html')