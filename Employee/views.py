import re
import random
import uuid
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# EMAIL FROM SETTINGS
from VirtualMain.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from datetime import datetime
from .forms import (AddUserForm)
from .models import UserDetails,RoleDetail,Course,Lesson,Lesson_Topic,CareerCategory,CFP_role,ProjectManager,AdminLicense,UserContact,UserEducation,CreateCourse

# Create your views here.
# ADMIN SECTION

@login_required
def adminDashboard(request):
    if request.user.is_staff and request.user.is_superuser:
        total_students=UserDetails.objects.all().count()
        total_sales=total_students*5000
        context={
            'total_students':total_students,
            'total_sales':total_sales,
        }
        return render(request,"Admin_pages/dashboard.html",context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def adminCourses(request):
    if request.user.is_staff and request.user.is_superuser:
        return render(request,'Admin_pages/courses.html')
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


@login_required
def adminAddcourse(request):
    if request.user.is_staff and request.user.is_superuser:
        return render(request,'Admin_pages/add-course.html')
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')
@login_required
def adminProjects(request):
    if request.user.is_staff and request.user.is_superuser:
        return render(request,'Admin_pages/projects.html')
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def adminRolecreation(request):
    if request.user.is_staff and request.user.is_superuser:
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

                role_user_password=request.POST['password']
                mail_subject = "[Activate Account] VE - Virtual Employee" \
                               "Temporary password : "

                send_mail(
                    mail_subject,
                    role_user_password,
                    EMAIL_HOST_USER,
                    [role_user_email],
                    fail_silently=False
                )
                try:

                    User.objects.create_user(username = role_user_name,email= role_user_email,first_name= user_firstname,
                                                    last_name = user_lastname,password = role_user_password,is_staff =True)

                    u_id = User.objects.get(username=role_user_name)
                    role = RoleDetail(user_id=u_id, role_user_id=role_user_id, user_role=user_role, role_user_name=role_user_name,
                                      role_user_email=role_user_email, role_user_password=role_user_password)
                    role.save()

                except:
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

            if 'roleSort' in request.POST:
                role = request.POST['roleSort']
                roled = RoleDetail.objects.filter(user_role=role)
                context ={
                    'roles':roled
                }
                return render(request, 'Admin_pages/role-creation.html', context)


        roles=RoleDetail.objects.order_by("-role_create_date")
        context={
            'roles':roles
        }
        return render(request,'Admin_pages/role-creation.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


def adminLicense(request):
    if request.user.is_staff and request.user.is_superuser:

        if request.method == 'POST':

            if 'category_submit' in request.POST:
                l_id = uuid.uuid4()
                key = l_id
                year = request.POST['year']
                data = AdminLicense(key=key,years=year)
                data.save()
                messages.success(request,"Key is generated")
                return redirect("adminLicense")
        keys = AdminLicense.objects.order_by('-date')
        context ={
            'keys' : keys
        }

        return render(request,"Admin_pages/admin_license.html",context)

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
        # Generating unique id
        num = random.randint(10000000, 99999999)
        str1 = 'VE'
        unique_id = str1+str(num)
        try:
            User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
            u_id = User.objects.get(username=username)
            addusr = UserDetails(user_id=u_id,user_pass=password,user_phone=userphone,user_unique=unique_id)
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
            if request.user.is_staff and request.user.is_superuser:
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
                            messages.error(request, "Error occured in Role")
                except:
                    messages.error(request, "login failed")
                    print("error")
                if request.user.is_active:
                    return redirect(userdashboard)
                    messages.success(request, 'Successfully loggedin')

        messages.error(request, "Login failed")
        return redirect('login')
    return render(request, 'virtualmain_pages/login.html')



def logout(request):
    auth.logout(request)
    return render(request,'Admin_pages/logout.html')

# USER SECTION

@login_required
def userdashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        course_data=Course.objects.all()
        context={
            'course_data':course_data,
        }
        return render(request,'virtualmain_pages/dashboard.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def userprofile(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        print(user.id)
        user_details = UserDetails.objects.get(user_id_id=user.pk)
        if UserEducation.objects.filter(user_id_id=user_details.pk).exists():
            user_education = UserEducation.objects.get(user_id_id=user_details.pk)
            context = {
                'user_education':user_education,
                'user_data': user_details
            }
            if UserContact.objects.filter(user_id_id=user_details.pk).exists():
                user_contact = UserContact.objects.get(user_id_id=user_details.pk)

                context={
                    'user_contact':user_contact,
                    'user_education': user_education,
                    'user_data': user_details
                }
                return render(request, "virtualmain_pages/user-profile.html", context)

            return render(request,"virtualmain_pages/user-profile.html",context)


        context = {
            'user_data' : user_details
        }
        return render(request,'virtualmain_pages/user-profile.html',context)

    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def userEdit(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:

        user = request.user
        user_detail = UserDetails.objects.get(user_id_id=user.id)
        # print(user_detail.pk)
        if request.method == 'POST':

            if 'contact' in request.POST:
                if UserContact.objects.filter(user_id_id=user_detail.pk).exists():
                    address1 = request.POST['address1']
                    address2 = request.POST['address2']
                    gender = request.POST['gender']
                    data = UserContact.objects.get(user_id_id=user_detail.pk)
                    data.address1 = address1
                    data.address2 = address2
                    data.gender = gender
                    data.save()
                    messages.success(request,"Updated Contact Info")
                    return redirect('userprofileEdit')

                else:
                    address1 = request.POST['address1']
                    address2 = request.POST['address2']
                    gender = request.POST['gender']

                    data = UserContact(address1=address1,address2=address2,gender=gender,user_id_id=user_detail.pk)
                    data.save()
                    messages.success(request,"Contact Info added")
                    return redirect(userEdit)
            if 'photo' in request.POST:
                try:
                    data = UserContact.objects.get(user_id_id=user_detail.pk)
                    if data.user_pic:
                        pic = request.FILES.get('user-profile-photo')
                        data.user_pic = pic
                        data.save()
                        messages.success(request,"Profile pic updated")
                    else:
                        pic = request.FILES.get('user-profile-photo')
                        data.user_pic = pic
                        data.save()
                        messages.success(request, "Profile pic added")
                except:
                    messages.error(request,"Complete your contact info to change Pic")
                    return redirect("userprofileEdit")
            if 'education' in request.POST:
                if UserEducation.objects.filter(user_id_id=user_detail.pk).exists():
                    print("exists")
                    course = request.POST['course']
                    special = request.POST['special']
                    year = request.POST['in_year']
                    inst_name = request.POST['in_name']
                    inst_address = request.POST['in_address']
                    edu = UserEducation.objects.get(user_id_id=user_detail.pk)
                    edu.degree = course
                    edu.specialization = special
                    edu.year = year
                    edu.institution = inst_name
                    edu.address =inst_address
                    edu.save()

                    messages.success(request, "Updated Education Info")
                    return redirect('userprofileEdit')


                else:
                    course = request.POST['course']
                    special = request.POST['special']
                    year = request.POST['in_year']
                    inst_name = request.POST['in_name']
                    inst_address = request.POST['in_address']
                    edu = UserEducation(degree=course,specialization=special,year=year,institution=inst_name,address=inst_address,user_id_id=user_detail.pk)
                    edu.save()
                    messages.success(request,"Education details added")



        if UserContact.objects.filter(user_id_id=user_detail.pk).exists():

            users = UserContact.objects.order_by("gender")

            context ={
                'user_detail' : user_detail,
                'users' : users,


            }
            if UserEducation.objects.filter(user_id_id=user_detail.pk).exists():

                users = UserContact.objects.order_by("gender")
                education = UserEducation.objects.order_by("degree")
                context = {
                    'user_detail': user_detail,
                    'users': users,
                    'education': education,

                }

                return render(request, 'virtualmain_pages/user-profile-edit.html', context)
            else:
                context ={
                    'user_detail': user_detail,
                    'users': users,
                    "edd":1
                }
                return render(request, 'virtualmain_pages/user-profile-edit.html', context)
            return render(request,'virtualmain_pages/user-profile-edit.html',context)
        else:
            context={
                "idd":1,
                "edd":1,


            }
            idd =1
            return render(request,'virtualmain_pages/user-profile-edit.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


def userProject(request):
    proj=ProjectManager.objects.all()
    context={
        "proj":proj
    }
    return render(request,'virtualmain_pages/user-project.html', context)

def userchangepassword(request):
    user = request.user
    details = UserDetails.objects.get(user_id_id=user.pk)
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        new_pass = request.POST['new_password1']
        try:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password Changed Successfully!')
                details.role_user_password = new_pass
                details.save()
                return redirect("/user-change-password/")
        except:
            messages.error(request, 'User is not able to change password !')

        else:
            messages.error(request,'Password not matching !')
            return redirect("/user-change-password/")
    context = {
        'form': form,
    }
    return render(request, "virtualmain_pages/user-change-pwd.html", context)

# CSM MODULE SECTION
@login_required
def csmDashboard(request):
    if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
        if request.user.is_authenticated:
            allCourses = Course.objects.filter(user=request.user)
            for i in allCourses:
                print(i.id)
            context ={
                'courses':allCourses,
            }
            return render(request, 'csm_pages/csm_dashboard.html',context)
    else:
        messages.error(request, "Wrong URL")
        return redirect('logout')

@login_required
def csmAddCourse(request):
    if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
        user = request.user
        data=CreateCourse.objects.get(create_id=0)
        if request.method == "POST":
            title = request.POST["title"]
            tagline  = request.POST["tagline"]
            short_description=request.POST["description"]
            image = request.FILES.get('course_image')
            category = request.POST["category"]
            role = request.POST["role"]
            course = request.POST["course"]
            difficulty_level = request.POST["difficulty_level"]
            # lesson_title=request.POST["lesson_title"]
            # topic=request.POST["topic"]
            meta_keywords = request.POST["meta_keywords"]
            meta_description = request.POST["meta_description"]
            course_points = request.POST["course_points"]
            certificate = request.POST["certificate"]
            # quiz and certificate details are not added yet

            #  Prerequisites
            requirements=request.POST["req"]
            learnings=request.POST["learn"]


            create = Course(user_id=user.id,title=title,tagline=tagline,short_description=short_description,
                           course_image=image,category=category,role=role,course=course,difficulty_level=difficulty_level,meta_keywords=meta_keywords,
                            meta_description=meta_description,course_points=course_points,certificate=certificate,requirements=requirements,learnings=learnings)
            create.save()

            obj=CreateCourse.objects.all()
            obj.delete()


            return redirect("/csmdashboard/")

        context={
            'data':data,
        }
        return render(request,'csm_pages/csm_add_course.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def csmEditCourse(request,id):
    if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
        c_id = id
        # print(c_id)
        datas = Course.objects.get(id = c_id)
        if request.method == "POST":
            title = request.POST["title"]
            tagline  = request.POST["tagline"]
            short_description=request.POST["description"]
            image = request.FILES.get('course_image')
            category = request.POST["category"]
            role = request.POST["role"]
            course = request.POST["course"]
            difficulty_level = request.POST["difficulty_level"]
            # lesson_title=request.POST["lesson_title"]
            # topic=request.POST["topic"]
            meta_keywords = request.POST["meta_keywords"]
            meta_description = request.POST["meta_description"]

            # Prerequisites
            requirements=request.POST['req']
            learnings=request.POST['learn']

            course_points = request.POST["course_points"]
            certificate = request.POST["certificate"]

            datas = Course.objects.get(id = c_id)

            datas.title=title
            datas.tagline=tagline
            datas.short_description=short_description
            datas.course_image=image
            datas.category=category
            datas.role=role
            datas.course=course
            datas.difficulty_level=difficulty_level
            datas.meta_keywords=meta_keywords
            datas.meta_description=meta_description
            datas.course_points=course_points
            datas.certificate=certificate
            datas.requirements=requirements
            datas.learnings=learnings
            datas.save()
            return redirect("/csmdashboard/")

        # Breakdown the requirements and learnings into list with help of python split()
        req_para=datas.requirements
        learn_para=datas.learnings

        req_list=req_para.split('_')
        learn_list=learn_para.split('_')

        context ={
            'datas' : datas,
            'req_list':req_list,
            'learn_list':learn_list,
        }
        return render(request,'csm_pages/csm_edit_course.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


@login_required
def csmAddCurriculam(request,id):
    if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
        c_id = id
        Course_name = Course.objects.get(id = c_id)
        course_title = Course_name.title
        if request.method =='POST':
            if 'create' in request.POST:
                lesson_name = request.POST['lesson']
                print(lesson_name)
                less_private = random.randint(112,1000)*100

                Less = Lesson(lesson_name=lesson_name,lesson_private=less_private,lesson_id_id=c_id)
                Less.save()
                messages.success(request,"Lesson Added")
                print("success")

            if 'addTopic' in request.POST:
                topic_caption = request.POST['topic_descrip']
                topic_video = request.FILES.get('topic_video')
                lesson = request.POST['les_id']
                try:
                    lesson_private = Lesson.objects.get(lesson_private=lesson)
                    if lesson_private:
                        print("enter")
                        topic = Lesson_Topic(topic_id_id=lesson_private.pk, topic_caption=topic_caption, topic_video= topic_video)
                        topic.save()
                        messages.success(request,"Topic added to lesson")
                    else:
                        messages.error(request,"Wrong Lesson Id")
                except:
                    print("error")
                    messages.error(request,"Some error occured")

            if 'del' in request.POST:
                print("delete")
                del_id = request.POST['l_id']
                try:
                    lesson_del =Lesson.objects.get(id = del_id).delete()
                    topic_del = Lesson_Topic.objects.filter(topic_id_id=del_id)
                    messages.success(request,"Deleted successfully")
                except:
                    messages.error(request,"Some error occured")

        lessons = Lesson.objects.order_by("lesson_name")
        context = {
            'lessons': lessons,
            'course_title': course_title,
        }
        print(course_title)
        return render(request,'csm_pages/csm_add_curriculam.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def csmEditLesson(request,id):
    if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
        lesson = Lesson.objects.get(id = id)
        print(lesson.lesson_name)
        topics = Lesson_Topic.objects.filter(topic_id_id=lesson.pk)
        if request.method == 'POST':
            if 'c_lesson' in request.POST:
                l_name = request.POST['lesson']
                lesson.lesson_name = l_name
                lesson.save()
                messages.success(request,"Lesson changed successfully")
            if 'topicEdit' in request.POST:
                topic_id = request.POST['unique_topic']
                caption = request.POST['topic_descrip']
                video = request.FILES.get('topic_video')
                print(topic_id)
                topic = Lesson_Topic.objects.get(id = topic_id)
                topic.topic_caption =caption
                topic.save()
                topic.topic_video =video
                if video:
                    topic.save()

                messages.success(request,"Topic changed sucessfully")
            if 'topicDelete' in request.POST:
                del_id = request.POST['del_id']
                print(del_id)
                delete = Lesson_Topic.objects.get(id = del_id).delete()
                messages.success(request,"Topic deleted")

        context ={
            'lesson' : lesson,
            'topics' : topics,
        }
        return render(request,'csm_pages/csm_edit_lesson.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

def csmSettings(request):
    user = request.user
    details = RoleDetail.objects.get(user_id_id=user.pk)
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        new_pass = request.POST['new_password1']
        try:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password Changed Successfully!')
                details.role_user_password = new_pass
                details.save()
                return redirect(csmSettings)
        except:
            messages.error(request, 'User is not able to change password !')

        else:
            messages.error(request,'Password not matching !')
            return redirect(csmSettings)
    context = {
        'form': form,
    }
    return render(request, "csm_pages/csm_settings.html", context)


# TL MODULE SECTION

def tlDashboard(request):
    return render(request,'TL_Pages/tl_dashboard.html')

def tlProjectDetails(request):
    return render(request,'TL_Pages/tl_project_details.html')

# PROJECT MODULE SECTION

def projectManager(request):
    if request.method == "POST":
        project_title=request.POST["project_title"]
        project_description=request.POST["project_description"]
        project_thumbnail=request.FILES.get("project_thumbnail")
        project_duration=request.POST["project_duration"]
        candidates_required=request.POST["candidates_required"]
        project_docs=request.FILES.get("project_docs")
        proj=ProjectManager.objects.create(
            project_title=project_title,
            project_description=project_description,
            project_thumbnail=project_thumbnail,
            project_duration=project_duration,
            candidates_required=candidates_required,
            project_docs=project_docs
        )
        proj.save()
        return redirect("/projectmanager/")
    return render(request,'ProjectModule_Pages/Project_manager.html')

def projectDashboard(request):
    project=ProjectManager.objects.all()
    return render(request,'ProjectModule_Pages/Project_dashboard.html',{"project":project})


@login_required
def cfp_create(request):

    if request.method=='POST':
        if 'category_submit' in request.POST:
            cag_name=request.POST['cagname']

            if CareerCategory.objects.filter(category=cag_name).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')

            if CareerCategory.objects.filter(category=cag_name.upper()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')

            if CareerCategory.objects.filter(category=cag_name.lower()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')

            if CareerCategory.objects.filter(category=cag_name.capitalize()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('cfp_create')


            category_id=CareerCategory.objects.all().count()+1
            cag_obj=CareerCategory(category_id=category_id,category=cag_name)
            cag_obj.save()

            return redirect('cfp_create')


        if 'cfp_submit' in request.POST:
            cfp_category=request.POST['cfp_cag']
            cfp_role=request.POST['cfp_role']
            cfp_course=request.POST['cfp_course']

            cfp_id=CFP_role.objects.all().count()+1
            cfp_obj=CFP_role(cfp_id=cfp_id,cfp_category=cfp_category,cfp_role=cfp_role,cfp_course=cfp_course)
            cfp_obj.save()
            messages.success(request, "Added to CFP")
            return redirect('cfp_create')
        if 'sortlist' in request.POST:
            cfp_category = request.POST['sortlist']
            roles = CFP_role.objects.filter(cfp_category=cfp_category)
            category_list = CareerCategory.objects.all()
            context ={
                'category_list': category_list,
                'cfp_list':roles,
            }
            return render(request, 'Admin_pages/cfp_create.html', context)

    category_list=CareerCategory.objects.all()

    cfp_list=CFP_role.objects.order_by("-cfp_create_date")

    context={
        'category_list':category_list,
        'cfp_list':cfp_list,
    }


    return render(request,'Admin_pages/cfp_create.html',context)




@login_required
def cfp_edit(request,id):
    cfp_id=id

    datas=CFP_role.objects.get(cfp_id=cfp_id)


    if request.method=="POST":
        if 'cfp_submit' in request.POST:
            cfp_category=request.POST['cfp_cag']
            cfp_role=request.POST['cfp_role']
            cfp_course=request.POST['cfp_course']

            datas=CFP_role.objects.get(cfp_id=cfp_id)
            datas.cfp_category=cfp_category
            datas.cfp_role=cfp_role
            datas.cfp_course=cfp_course
            datas.save()

            return redirect('/cfp_create/')

        if 'cfp_delete' in request.POST:
            delete_id=request.POST['delete_id']
            obj=CFP_role.objects.filter(cfp_id=delete_id)
            obj.delete()

            return redirect('cfp_create')


    category_list=CareerCategory.objects.all()

    role_str=datas.cfp_course
    role_list=role_str.split('_')
    context={
        'datas':datas,
        'role_list':role_list,
        'category_list':category_list,
    }

    return render(request,'Admin_pages/cfp_edit.html',context);


@login_required
def category_edit(request,id):
    category_id=id
    datas=CareerCategory.objects.get(category_id=category_id)
    name=datas.category

    if request.method=="POST":
        if 'category_submit' in request.POST:
            category=request.POST['category_name']

            datas=CareerCategory.objects.get(category_id=category_id)

            datas.category=category
            datas.save()

            CFP_role.objects.filter(cfp_category=name).update(cfp_category=category)
            return redirect('/cfp_create/')

    context={
        'datas':datas,
    }
    return render(request,'Admin_pages/category_edit.html',context)



def test(request):
    if request.method=='POST':
        if 'category' in request.POST:
            count=CreateCourse.objects.all().count()
            if count==0:
                cag=request.POST['category']
                data=CreateCourse(create_category=cag)
                data.save()
                return redirect('/test/')

            else:
                cag=request.POST['category']
                data=CreateCourse.objects.get(create_id=0)
                data.create_category=cag
                data.save()
                return redirect('/test/')


        if 'role' in request.POST:
            c_course=request.POST['c_course']
            role=request.POST['role']
            data=CreateCourse.objects.get(create_category=c_course)
            data.create_role=role
            data.save()
            return redirect('/test/')

        if 'course-submit' in request.POST:
            confirm_cag=request.POST['confirm_cag']
            confirm_role=request.POST['confirm_role']
            confirm_course=request.POST['confirm_course']

            check=CFP_role.objects.get(cfp_role=confirm_role)
            if check.cfp_category != confirm_cag:
                messages.error(request, 'The Category do not match with CFP Role')
                return redirect('/test/')
            else:
                data=CreateCourse.objects.get(create_role=confirm_role)
                data.create_course=confirm_course
                data.save()
                messages.success(request,"Course Successfully Created Check Database")
                return redirect('/csmaddcourse/')
            return redirect('/test/')

    cag_data=CareerCategory.objects.all()
    if CreateCourse.objects.count()!=0:
        obj=CreateCourse.objects.get(create_id=0)
        role_list=CFP_role.objects.filter(cfp_category=obj.create_category)
        try:
            course_text=CFP_role.objects.get(cfp_role=obj.create_role)
            course_list=course_text.cfp_course.split('_')
        except:
            course_list=[]
    else:
        obj="Choose"
        role_list=[]
        course_list=[]

    context={
        'cag_data':cag_data,
        'obj':obj,
        'role_list':role_list,
        'course_list':course_list
    }
    return render(request,'csm_pages/test.html',context)
