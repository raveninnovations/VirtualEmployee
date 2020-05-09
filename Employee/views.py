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
    if request.method=='POST':

        # When we Press Create Role Button
        if 'create' in request.POST:
            # Assigning Unique Id To each role
            user_role=request.POST['role']
            if user_role=="CSM":
                role_user_id="CM"+str(100+(RoleDetail.objects.filter(user_role="CSM").count()+1))
            elif user_role=="PCM":
                role_user_id="PM"+str(200+(RoleDetail.objects.filter(user_role="PCM").count()+1))
            elif user_role=="TL":
                role_user_id="TL"+str(300+(RoleDetail.objects.filter(user_role="TL").count()+1))
            elif user_role=="Instructor":
                role_user_id="IN"+str(400+(RoleDetail.objects.filter(user_role="Instructor").count()+1))
            else:
                role_user_id=000


            role_user_name=request.POST['username']
            role_user_email=request.POST['email']
            # Send Mail
            # send_mail(
            #     "New Account Setup",
            #     "There has been an acount setup",
            #     "akashsingh11112011@gmail.com",
            #     [role_user_email,'rahul.agarwal31101999@gmail.com'],
            #     fail_silently=False
            # )

            role_user_password=request.POST['password']

            # Saving the role input in the model
            role=RoleDetail(role_user_id=role_user_id,user_role=user_role,role_user_name=role_user_name,role_user_email=role_user_email,role_user_password=role_user_password)
            role.save()



            return redirect("adminrolecreation")


        # When we press Remove Button
        if 'delete' in request.POST:
            del_id=request.POST['del_id']
            roled=RoleDetail.objects.get(role_user_id=del_id).delete()
            return redirect('adminrolecreation')



    roles=RoleDetail.objects.order_by("-role_create_date")
    context={
        'roles':roles
    }

    return render(request,'Admin_pages/role-creation.html',context)



def adduser(request):
    form = AddUserForm
    if request.method =='POST':
        firstname = request.POST['first']
        lastname = request.POST['last']
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
            messages.error(request, 'Firstname cannot have numbers')
            return redirect('register')
        if lastname.isdigit():
            messages.error(request, 'Lastname cannot have numbers')
            return redirect('register')
        if regex.search(firstname):
            messages.error(request, 'firstname cannot have special characters')
            return redirect('register')
        if regex.search(lastname):
            messages.error(request, 'lastname cannot have special characters')
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

    return render(request,'virtualmain_pages/user-profile-edit.html')



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
