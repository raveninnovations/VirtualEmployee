import re
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from .forms import (AddUserForm)
from .models import UserDetails,RoleDetail,Course

from django.core.mail import send_mail
# Create your views here.
# ADMIN SECTION

@login_required
def adminDashboard(request):
    total_students=UserDetails.objects.all().count()
    total_sales=total_students*5000
    context={
        'total_students':total_students,
        'total_sales':total_sales,
    }
    return render(request,"Admin_pages/dashboard.html",context)


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

            user_firstname = request.POST['fname']
            user_lastname = request.POST['lname']
            role_user_name=request.POST['email']
            role_user_email=request.POST['email']
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if User.objects.filter(email=role_user_email).exists():
                messages.error(request, 'The email already exists')
                return redirect('adminrolecreation')
            if User.objects.filter(username=role_user_name).exists():
                messages.error(request, 'That username is being used')
                return redirect('adminrolecreation')
            if user_firstname.isdigit():
                messages.error(request, 'Firstname cannot have numbers')
                return redirect('adminrolecreation')
            if regex.search(user_firstname):
                messages.error(request, 'Firstname cannot have special characters')
                return redirect('adminrolecreation')
            if user_lastname.isdigit():
                messages.error(request, 'Lastname cannot have numbers')
                return redirect('adminrolecreation')
            if regex.search(user_lastname):
                messages.error(request, 'Lastname cannot have special characters')
                return redirect('adminrolecreation')

            # Send Mail
            # send_mail(
            #     "New Account Setup",
            #     "There has been an acount setup",
            #     "akashsingh11112011@gmail.com",
            #     [role_user_email,'rahul.agarwal31101999@gmail.com'],
            #     fail_silently=False
            # )

            role_user_password=request.POST['password']

            try:
                User.objects.create_user(username = role_user_name,email= role_user_email,first_name= user_firstname,
                                                last_name = user_lastname,password = role_user_password)
                u_id = User.objects.get(username=role_user_name)
                role = RoleDetail(user_id=u_id, role_user_id=role_user_id, user_role=user_role, role_user_name=role_user_name,
                                  role_user_email=role_user_email, role_user_password=role_user_password)
                role.save()

            except:
                print("hai")
                print("error")
                messages.error(request,"Some error occured")
                return redirect("adminaddcourse")
            # Saving the role input in the model
            messages.success(request,"Submitted successfully")
            return redirect("adminrolecreation")

        # When we press Remove Button
        if 'delete' in request.POST:
            del_id=request.POST['del_id']
            roled=RoleDetail.objects.get(user_id_id=del_id).delete()
            # Delete from the user table
            user_del = User.objects.get(id=del_id).delete()
            messages.success(request,"Deleted success")
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
        # Roles

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                print('Welcome admin')
                return redirect(adminDashboard)
            else:
                try:
                    print("user role")
                    if RoleDetail.objects.filter(role_user_email=email, role_user_password=password).exists():
                        print("user role")
                        role = RoleDetail.objects.get(role_user_email=email)
                        if role.user_role == "CSM":
                            return redirect('csmDashboard')
                        elif role.user_role == "TL":
                            print("TL PAGE")
                        else:
                            messages.error(request,"Error occured in Role")
                except:
                    messages.error(request, "login failed")
                    print("error")
                if request.user.is_active:
                    return redirect(userdashboard)
                    messages.success(request, 'Successfully loggedin')

        messages.error(request, "Login failed")
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
@login_required
def csmDashboard(request):
    if request.user.is_authenticated:
        allCourses = Course.objects.filter(user=request.user)
        for i in allCourses:
            print(i.id)
        context ={
            'courses':allCourses,
        }
        return render(request,'csm_pages/csm_dashboard.html',context)

@login_required
def csmAddCourse(request):
    user = request.user
    if request.method == "POST":
        title = request.POST["title"]
        tagline  = request.POST["tagline"]
        short_description=request.POST["description"]
        image = request.FILES.get('course_image')
        category = request.POST["category"]
        difficulty_level = request.POST["difficulty_level"]
        # lesson_title=request.POST["lesson_title"]
        # topic=request.POST["topic"]
        meta_keywords = request.POST["meta_keywords"]
        meta_description = request.POST["meta_description"]
        course_points = request.POST["course_points"]
        certificate = request.POST["certificate"]
        # quiz and certificate details are not added yet   
        create = Course(user_id=user.id,title=title,tagline=tagline,short_description=short_description,
                       course_image=image,category=category,difficulty_level=difficulty_level,meta_keywords=meta_keywords,
                        meta_description=meta_description,course_points=course_points,certificate=certificate)
        create.save()


        return redirect("/csmdashboard/")
    return render(request,'csm_pages/csm_add_course.html')

@login_required
def csmEditCourse(request,id):
    c_id = id
    print(c_id)
    datas = Course.objects.get(id = c_id)
    context ={
        'datas' : datas
    }
    return render(request,'csm_pages/csm_edit_course.html',context)

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


