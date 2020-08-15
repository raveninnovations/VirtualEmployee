import cv2 as cv
from PIL import Image
import openpyxl
import datetime as dt
import datetime
import re
import random, math
import uuid

from datetime import datetime
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404

from moviepy.editor import VideoFileClip
# EMAIL FROM SETTINGS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from VirtualMain.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage

from datetime import datetime
from .forms import (AddUserForm)


from .models import UserDetails, RoleDetail, Course, Lesson, Lesson_Topic, CareerCategory, CFP_role,ProjectManager,AdminLicense,UserContact,UserEducation,CreateCourse,CareerChoice,StudentCFP,ProjectCFPStore,ProgressCourse,UsedLicense,EnrolledProject,watched,Claim,CourseTag,ProjectPoint,UserWorkExperience,UserSkill,Certificate,Reference,BlogManager,BlogCategory


# Create your views here.
# ADMIN SECTION

def landing(request):
    return render(request,'virtualmain_pages/landing.html')


@login_required
def adminDashboard(request):
    user=request.user
    user_email = "ravencorporations@gmail.com"
    # admindash=AdminLicense.objects.get(adminuser=request.user)
    if request.user.is_staff and request.user.is_superuser:
        total_students=UserDetails.objects.all().count()
        total_sales=total_students*5000
        if request.method == 'POST':
            num = 1012
            if 'requestotp' in request.POST:
                print("hai")
                OTP = random.randint(99, 9999)
                request.session['num'] = OTP
                print(OTP)
                mail_subject = "OTP for Admin License Page"
                message = f'Hi,{request.user.first_name} is requesting for an OTP to access Admin License page, please share this OTP : {OTP}'
                email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[user_email,])
                email.send()
                messages.success(request,'Contact admin for OTP')

            if 'obtainedotp' in request.POST:
                new_otp = request.session['num']
                receivedOtp=request.POST["receivedOtp"]
                print(receivedOtp)
                print(new_otp)
                if int(receivedOtp) == new_otp:
                    messages.success(request,'Welcome')
                    return redirect('adminLicense')

                else:
                    messages.error(request, "OTP mismatched")


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

        if request.user.is_authenticated:
            allCourses = Course.objects.all()

            context ={
                'courses':allCourses,
            }
        return render(request,'Admin_pages/courses.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')
@login_required
def adminProjects(request):
    if request.user.is_staff and request.user.is_superuser:
        projects=ProjectManager.objects.all()
        context={
            'projects':projects,
        }
        return render(request,'Admin_pages/projects.html',context)
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
                elif user_role == "Blogger":
                    role_user_id  = "Blog"+str(500+(RoleDetail.objects.filter(user_role="Blogger").count()+1))
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
                mail_subject = "[Activate Account] VE - Virtual Employee"
                current_site = get_current_site(request)
                message = render_to_string('virtualmain_pages/user_info.html', {
                    'user': role_user_email,
                    'firstname': user_firstname,
                    'lastname': user_lastname,
                    'domain': current_site.domain,
                    'pass': role_user_password,
                })
                email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[role_user_email])
                email.send()
                try:

                    user=User.objects.create_user(username = role_user_name,email= role_user_email,first_name= user_firstname,
                                                    last_name = user_lastname,password = role_user_password)
                    if user_role == "CSM":
                        user.is_staff = True
                    elif user_role == "TL":
                        user.is_staff = False
                        user.is_superuser = True
                    elif user_role == "Blogger":
                        user.is_active =True
                        user.is_staff = False
                        user.is_superuser = False
                    elif user_role == "PCM":
                        user.is_superuser=True
                        user.is_staff = False
                    user.save()
                    u_id = User.objects.get(username=role_user_name)
                    role = RoleDetail(user_id=u_id, role_user_id=role_user_id, user_role=user_role, role_user_name=role_user_name,
                                      role_user_email=role_user_email, role_user_password=role_user_password)
                    role.save()

                except:
                    messages.error(request,"Some error occured")
                    return redirect("adminrolecreation")
                # Saving the role input in the model
                messages.success(request,"Email has been sent successfully")
                return redirect("adminrolecreation")

            # When we press Remove Button
            if 'delete' in request.POST:
                del_id=request.POST['del_id']

                if RoleDetail.objects.filter(role_user_id=del_id).exists():
                    main_id_1 =RoleDetail.objects.get(role_user_id=del_id)
                    main_id = main_id_1.user_id_id
                    roled=RoleDetail.objects.get(role_user_id=del_id).delete()
                    # Delete from the user table
                    user_del = User.objects.get(id=main_id).delete()
                    messages.success(request,"Deleted success")
                else:
                    messages.error(request,"Some error occured")
                return redirect('adminrolecreation')

            if 'roleSort' in request.POST:
                role = request.POST['roleSort']
                if role == 'ALL':
                    roled=RoleDetail.objects.all()
                else:
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

@login_required
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
        u_keys = UsedLicense.objects.order_by('-u_date')
        context ={
            'keys' : keys,
            'u_keys':u_keys
        }

        return render(request,"Admin_pages/admin_license.html",context)

@login_required
def adminLicenseInfo(request,id):
    if request.user.is_staff and request.user.is_superuser:
        print(id)
        license_info = UsedLicense.objects.get(id = id)
        try:
            student_info = UserDetails.objects.get(user_license=license_info.u_key)
            delta = dt.timedelta(days=366)
            license_year = license_info.u_years * delta
            today =dt.datetime.now().date()
            print(license_info.u_date.date())
            print(today)
            days_over = today - student_info.user_date.date()
            print(days_over)
            print("Days left")
            days_left = license_year - days_over
            print(days_left)

            context = {
                'student': student_info,
                'license': license_info,
                'today':today,
                'days_over':days_over,
                'days_left':days_left,
            }
            return render(request, 'Admin_pages/admin_license_info.html', context)

        except:
            print("error")

        return render(request,'Admin_pages/admin_license_info.html')
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')

@login_required
def adminStudents(request):

    students = UserDetails.objects.order_by('-user_date')
    students_contact = UserContact.objects.all()

    if request.method == 'POST':
        if 'id_search' in request.POST:
            emp_id = request.POST['id_search']
            if UserDetails.objects.filter(user_unique=emp_id).exists():
                print("Exists")
                students = UserDetails.objects.filter(user_unique=emp_id)

    context={
        'students':students,
        'students_contact':students_contact,
        # 'my_words':my_words,
    }
    return render(request,'Admin_pages/admin_students.html',context)

# def delete_student(request, student_id):
# 	student_instance = UserDetails.objects.get(pk=student_id)
# 	student_instance.delete()

# 	return redirect("/admindashboard/student_info/")

def adduser(request):
    form = AddUserForm
    # lisences = AdminLicense.objects.all()
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
        # Generating reference id
        ref = random.randint(54866,9854721)
        str2 =  firstname
        reference_id = str2+str(ref)


        try:
            # if license_key:
            #     if AdminLicense.objects.filter(key=license_key).exists():
            #         key = AdminLicense.objects.get(key=license_key)
            #         if UsedLicense.objects.filter(u_key=key).exists():
            #             print("Key is Used")
            #             messages.error(request,"Key is already applied")
            #             return redirect('register')
            #         else:
            #             used_key = UsedLicense(u_key=key.key,u_years=key.years)
            #             used_key.save()
            #             key.delete()
            #             messages.success(request,"License Key applied ! You can login")
            #
            #     else:
            #         messages.error(request,'License Key Not Valid')
            #         return redirect('register')
            # else:
            license_key =None
            User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
            u_id = User.objects.get(username=username)
            addusr = UserDetails(user_id=u_id,user_pass=password,user_phone=userphone,user_unique=unique_id,user_license=license_key)
            addusr.save()
            ref_user = Reference(user_id=u_id,ref_id=reference_id,used_peoples=None,used_id=None)
            ref_user.save()

            # if license_key:
            #
            #     return redirect('login')
            # else:
            #     return redirect('pricing')

        except:
            usr = User.objects.get(username=email)
            usr.delete()
            messages.error(request, 'Some error occured !')
            return redirect('register')
        messages.success(request, 'User Added!')
        return redirect('dashboard')
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
                    if RoleDetail.objects.filter(role_user_email=email).exists():
                        print("user role")
                        role = RoleDetail.objects.get(role_user_email=email)
                        if role.user_role == "CSM":
                            return redirect('csmDashboard')
                        elif role.user_role == "TL":
                            return redirect('tlDashboard')
                        elif role.user_role == "PCM":
                            return redirect('projectDashboard')
                        elif role.user_role == "Instructor":
                            return redirect('insDashboard')
                        elif role.user_role == "Blogger":
                            return redirect('blogManager')
                        else:
                            messages.error(request, "Error occured in Role")
                except:
                    messages.error(request, "login failed")
                    print("error")
                if request.user.is_active:
                    try:
                        license = UserDetails.objects.get(user_id_id=user.pk)
                        if license.user_license:
                            print("license key added")
                        else:
                            print("No license key")
                            messages.success(request, "Apply License Key")
                            return redirect('activatecode')
                    except:
                        messages.error(request,"Dont have permission to login")
                        return redirect('login')
                    try:
                        user_cfp = UserDetails.objects.get(user_id_id=user.pk)
                        if user_cfp.user_cfp == False:
                            user_cfp.user_cfp = True
                            user_cfp.save()
                            messages.success(request,"Choose your career focus path ! Enjoy")
                            return redirect('usercfp')
                        else:
                            return redirect(userdashboard)
                    except:
                        user_cfp = UserDetails.objects.get(user_id_id=user.pk)
                        user_cfp.user_cfp = True
                    return redirect(userdashboard)
        messages.error(request, "Login failed")
        return redirect('login')
    return render(request, 'virtualmain_pages/login.html')



def user_logout(request):
    print("hello")
    auth.logout(request)
    print("hai")
    return render(request,'Admin_pages/logout.html')



def activatecode(request):
    user_id = request.user.pk
    license = AdminLicense.objects.all()
    try:
        user = UserDetails.objects.get(user_id = user_id)
        print(user.user_license)
    except:
        print("Error")
        messages.success(request,"Some error occured")
    if request.method == "POST":
        license_key = request.POST['license']
        if license_key:
            if AdminLicense.objects.filter(key=license_key).exists():
                key = AdminLicense.objects.get(key=license_key)
                if UsedLicense.objects.filter(u_key=key).exists():
                    print("Key is Used")
                    messages.error(request,"Key is already applied")
                    return redirect('register')
                else:
                    used_key = UsedLicense(u_key=key.key,u_years=key.years)
                    used_key.save()
                    user.user_license = license_key
                    user.save()
                    key.delete()
                    messages.success(request,"License Key applied !")
                    return redirect('usercfp')

            else:
                messages.error(request,'License Key Not Valid')
                return redirect('activatecode')
        else:
            license_key = None

    return render(request,'virtualmain_pages/activationcode.html')


# USER SECTION

@login_required
def userdashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user

        user_details = UserDetails.objects.get(user_id_id=user.pk)
        course_data = Course.objects.all()

        try:
            if StudentCFP.objects.filter(user_id_id=user_details.pk).exists():

                cfp_details = StudentCFP.objects.get(user_id_id=user_details.pk)

                # CFP  COURSES
                lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)
                lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)

                #Displaying Projects
                projects1=ProjectManager.objects.filter(project_category=cfp_details.category_one)
                projects2=ProjectManager.objects.filter(project_category=cfp_details.category_two)
                cfp1_projects=[]
                cfp2_projects=[]
                for i in projects1:
                    res=i.project_cfp.find(cfp_details.role_one)
                    if res != -1:
                        cfp1_projects.append(i)

                for j in projects2:
                    res=j.project_cfp.find(cfp_details.role_two)
                    if res != -1:
                        cfp2_projects.append(j)
                if ProgressCourse.objects.filter(user_id=user.pk).exists():

                    progress_course = ProgressCourse.objects.filter(user=user)
                else:
                    progress_course = None

                blog_cag=BlogCategory.objects.all()
                blogs=BlogManager.objects.all()

                context = {
                    'cfp_details':cfp_details,
                    'lists':lists,
                    'lists2':lists2,
                    'course_data': course_data,
                    'progress_course':progress_course,
                    'cfp1_projects':cfp1_projects,
                    'cfp2_projects':cfp2_projects,
                    'blog_cag':blog_cag,
                    'blogs':blogs

                }
                return render(request, 'virtualmain_pages/dashboard.html', context)
            else:
                return render(request,'virtualmain_pages/dashboard.html')

        except:
            print("Error in dashboard")

        context={
            'course_data':course_data,

        }
        return render(request,'virtualmain_pages/dashboard.html', context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def userCourse(request,id):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        course_details = Course.objects.get(id = id)
        print(course_details.pk)
        lessons = Lesson.objects.filter(lesson_id_id=course_details.pk)
        topics = Lesson_Topic.objects.all()

        req_str=course_details.requirements
        req_list=req_str.split('_')

        learn_str=course_details.learnings
        learn_list=learn_str.split('_')
        context ={
            'course_details':course_details,
            'lessons': lessons,
            'topics': topics,
            'req_list':req_list,
            'learn_list':learn_list
        }

        return render(request,"virtualmain_pages/user_course_intro.html",context)
    else:
        messages.error(request,"Wrong url")
        return redirect('login')


def userLesson(request,id):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        print(id)
        user = request.user
        user_details = UserDetails.objects.get(user_id_id=user.pk)
        course_details = Course.objects.get(id = id)
        lessons = Lesson.objects.filter(lesson_id_id=course_details.pk)
        topics = Lesson_Topic.objects.all()
        saves = watched.objects.all()
        t_video =None
        if request.method=='POST':
            if 'add' in request.POST:
                total_topics = []
                for i in lessons:
                    topic = Lesson_Topic.objects.filter(topic_id_id=i.id)
                    for j in topic:
                        print(j.id)
                        total_topics.append(j.id)
                print(len(total_topics))
                obj = ProgressCourse(user=user, course_id=id, title=course_details.title,
                                     category=course_details.category,
                                     role=course_details.role, course=course_details.course,
                                     course_image=course_details.course_image, topics_count=len(total_topics))
                obj.save()
                return redirect(request.path_info)

            if 'video' in request.POST:
                name = request.POST['video']
                t_video = Lesson_Topic.objects.get(topic_caption=name)
                if not watched.objects.filter(video=t_video.pk,user_id=user_details.pk).exists():
                    save = watched(status="watched",video_id=t_video.pk,course_id=course_details.pk,user_id=user_details.pk)
                    save.save()

            if 'claim' in request.POST:
                print("claim rewards")
                try:

                    if not Claim.objects.filter(claim_id_id = course_details.pk,user_id=user_details.pk).exists():

                        claim = Claim(claim_id_id=course_details.pk,category=course_details.category,course_tag=course_details.course,points=course_details.course_points,user_id=user_details.pk)
                        claim.save()
                        points = Claim.objects.filter(course_tag=course_details.course, user_id=user_details.pk)
                        if points:
                            total = 0
                            for point in points:
                                print("hlo")
                                print(point.points)
                                total += int(point.points)
                            if total > 300:
                                course_del = Claim.objects.filter(user_id=user_details.pk,claim_id_id=course_details.pk)
                                course_del.delete()
                                messages.error(request,"Rewards reached maximum")
                                return redirect('userlesson',id)

                        if CourseTag.objects.filter(user_id_id=user_details.pk,
                                                    course_tag=course_details.course).exists():

                            points = CourseTag.objects.get(user_id_id=user_details.pk,course_tag=course_details.course)

                            c_points = course_details.course_points
                            new_points = int(points.points) + int(c_points)

                            points.points = new_points
                            points.save()
                        else:
                            new_points = course_details.course_points
                            tag = CourseTag(points=new_points,user_id_id=user_details.pk,course_tag=course_details.course,course_role=course_details.role)
                            tag.save()

                        messages.success(request,"Rewards Credited")
                    else:
                        messages.error(request,"Claim already done")
                        print("claim done already")







                except:
                    messages.error(request,"Claim failed")
        progress=None
        if ProgressCourse.objects.filter(user_id=user.pk, course_id=id).exists():
            try:
                progress = ProgressCourse.objects.get(user= user,course_id=id)
                print(progress.topics_count)

                count=watched.objects.filter(course_id=progress.course_id,user_id=user_details.pk)
                print("new")
                if count.count() == progress.topics_count:
                    progress = progress.topics_count
                else:
                    print("not executed")
                    progress = None
            except:
                progress =None
            check=1
            print("ok")
        else:
            check=0
            print("no")

        context ={
            'course_details':course_details,
            'user_details':user_details,
            'lessons': lessons,
            'topics': topics,
            'check':check,
            't_video':t_video,
            'watch': saves,
            'progress':progress,
        }

    return render(request,'virtualmain_pages/user_course_lesson.html',context)

@login_required
def userprofile(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        user_details = UserDetails.objects.get(user_id_id=user.pk)
        if Reference.objects.filter(user_id=user.pk).exists():
            reference = Reference.objects.get(user_id=user.pk)
            reference = reference.ref_id
        else:
            reference = "Key not provided"

        courses = Course.objects.all()
        claim = Claim.objects.all()
        tag = CourseTag.objects.filter(user_id_id=user_details.pk)
        # For courses completed
        com_courses = None
        tot_achiev = 0
        if Claim.objects.filter(user_id=user_details.pk).exists():
            com_courses = Claim.objects.filter(user_id = user_details.pk).count()
            tot_achiev += int(com_courses)
            print(com_courses)

        if ProjectPoint.objects.filter(user_id_id=user_details.pk).exists():
            proj_point = ProjectPoint.objects.filter(user_id_id=user_details.pk)
        else:
            proj_point = None
        if UserEducation.objects.filter(user_id_id=user_details.pk).exists():
            user_education = UserEducation.objects.filter(user_id_id=user_details.pk)
            try:
                work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
            except:
                work=[]

            try:
                tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
            except:
                tech_skills=[]

            try:
                man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
            except:
                man_skills=[]

            try:
                lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
            except:
                lan_skills=[]


            # Certificate Retrieval
            #
            # certificate=Certificate.objects.filter(user_id_id=user_contact.pk)


            context = {
                'user_education':user_education,
                'user_data': user_details,
                'work': work,
                'tech_skills':tech_skills,
                'man_skills':man_skills,
                'lan_skills':lan_skills,
                'com_courses':com_courses,
                'tot_achiev':tot_achiev,
                'reference':reference,
                # 'certificate':certificate

            }
            if UserContact.objects.filter(user_id_id=user_details.pk).exists():
                user_contact = UserContact.objects.get(user_id_id=user_details.pk)
                try:
                    work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
                except:
                    work=[]


                try:
                    tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
                except:
                    tech_skills=[]

                try:
                    man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
                except:
                    man_skills=[]

                try:
                    lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
                except:
                    lan_skills=[]

                # Certificate Retrieval

                certificate=Certificate.objects.filter(user_id_id=user_contact.pk)


                context={
                    'user_contact':user_contact,
                    'user_education': user_education,
                    'user_data': user_details,
                    'work':work,
                    'tech_skills':tech_skills,
                    'man_skills':man_skills,
                    'lan_skills':lan_skills,
                    'certificate':certificate,
                    'com_courses': com_courses,
                    'tot_achiev': tot_achiev,
                    'reference': reference,

                }
                # CFP
                if StudentCFP.objects.filter(user_id_id=user_details.pk).exists():
                    cfp_details = StudentCFP.objects.get(user_id_id=user_details.pk)
                    # CFP  COURSES
                    lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)
                    lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)
                    try:
                        work = UserWorkExperience.objects.filter(user_id_id=user_details.pk).order_by("-start_year")
                    except:
                        work=[]

                    try:
                        tech_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Technical')
                    except:
                        tech_skills=[]

                    try:
                        man_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Management')
                    except:
                        man_skills=[]

                    try:
                        lan_skills=UserSkill.objects.filter(user_id_id=user_details.pk,category='Languages')
                    except:
                        lan_skills=[]


                    # Certificate Retrieval

                    certificate=Certificate.objects.filter(user_id_id=user_contact.pk)

                    certi1 = Certificate.objects.filter(user_id_id=user_contact.pk , certi_choose= 1)
                    certi2 = Certificate.objects.filter(user_id_id=user_contact.pk , certi_choose= 2)


                    # print('work:', work)

                    context = {
                        'cfp_details': cfp_details,
                        'user_data': user_details,
                        'user_contact': user_contact,
                        'user_education': user_education,
                        'lists': lists,
                        'lists2': lists2,
                        'claims' :claim,
                        'tag':tag,
                        'proj':proj_point,
                        'work':work,
                        'tech_skills':tech_skills,
                        'man_skills':man_skills,
                        'lan_skills':lan_skills,
                        'certificate':certificate,
                        'certi1' : certi1,
                        'certi2' : certi2,
                        'com_courses': com_courses,
                        'tot_achiev': tot_achiev,
                        'reference': reference,


                    }
                    if request.method == "POST":
                        if 'cfp1_m1' in request.POST:
                            data=Certificate.objects.filter(name__isnull=True,serial_key__isnull=True,email__isnull=True,issue_date__isnull=True)
                            # data=Certificate.objects.all()
                            data.delete()

                            template_path = 'static/images/ceritficate.png'
                            output_path ='media/certificates/'
                            print(template_path)
                            font_size = 3
                            font_color = (1, 0, 4)
                            coordinate_y_adjustment = 14
                            coordinate_x_adjustment = -800
                            topic_y = -290
                            topic_x = -800

                            date_y = -730
                            date_x = -620

                            certi_name = user.first_name +" " +user.last_name
                            certi_name = certi_name.upper()
                            certi_topic = cfp_details.role_one
                            certi_topic = certi_topic.upper()
                            certi_date = datetime.today()

                            certi_date = certi_date.strftime('%m/%d/%Y')
                            # read the certificate template
                            img = cv.imread(template_path)

                            # choose the font from opencv
                            font = cv.FONT_ITALIC

                            # get the size of the name to be
                            # printed
                            text_size = cv.getTextSize(certi_name, font, font_size, 10)[0]
                            text_x = (img.shape[1] - text_size[0]) / 2 + coordinate_x_adjustment
                            text_y = (img.shape[0] + text_size[1]) / 2 - coordinate_y_adjustment
                            text_x = int(text_x)
                            text_y = int(text_y)
                            cv.putText(img, certi_name,
                                       (text_x, text_y),
                                       font,
                                       font_size,
                                       font_color, 10)
                            # for topic
                            text_x = (img.shape[1] - text_size[0]) / 2 + topic_x
                            text_y = (img.shape[0] + text_size[1]) / 2 - topic_y
                            text_x = int(text_x)
                            text_y = int(text_y)
                            cv.putText(img, certi_topic,
                                       (text_x, text_y),
                                       font,
                                       2,
                                       font_color, 10)

                            text_x = (img.shape[1] - text_size[0]) / 2 + date_x
                            text_y = (img.shape[0] + text_size[1]) / 2 - date_y
                            text_x = int(text_x)
                            text_y = int(text_y)
                            cv.putText(img, certi_date,
                                       (text_x, text_y),
                                       font,
                                       2,
                                       font_color, 10)
                            certi_path = output_path+user_contact.user_id.user_id.first_name + '.png'
                            rough = 'certificates/'+user_contact.user_id.user_id.first_name + '.png'
                            cv.imwrite(certi_path, img)

                            certificate = certi_path

                            print(certificate)
                            # data = Certificate.objects.get(user_id_id=user_contact.pk)
                            # data.delete()
                            credential = random.randint(125,955842)*10
                            data = Certificate(user_id_id=user_contact.pk,name=certi_name,certi_topic=certi_topic,issue_date=certi_date,email=user.email,certi_img=rough,serial_key=credential,certi_choose=1)
                            data.save()

                            messages.success(request,"Certificate Generated")
                            return redirect(request.path_info)

                        if 'cfp2_m1' in request.POST:
                            data = Certificate.objects.filter(name__isnull=True, serial_key__isnull=True,
                                                              email__isnull=True, issue_date__isnull=True)
                            # data=Certificate.objects.all()
                            data.delete()

                            template_path = 'static/images/ceritficate.png'
                            output_path = 'media/certificates/'
                            print(template_path)
                            font_size = 3
                            font_color = (1, 0, 4)
                            coordinate_y_adjustment = 14
                            coordinate_x_adjustment = -800
                            topic_y = -290
                            topic_x = -800

                            date_y = -730
                            date_x = -620

                            certi_name = user.first_name + " " + user.last_name
                            certi_name = certi_name.upper()
                            certi_topic = cfp_details.role_two
                            certi_topic = certi_topic.upper()
                            certi_date = datetime.today()

                            certi_date = certi_date.strftime('%m/%d/%Y')
                            # read the certificate template
                            img = cv.imread(template_path)

                            # choose the font from opencv
                            font = cv.FONT_ITALIC

                            # get the size of the name to be
                            # printed
                            text_size = cv.getTextSize(certi_name, font, font_size, 10)[0]
                            text_x = (img.shape[1] - text_size[0]) / 2 + coordinate_x_adjustment
                            text_y = (img.shape[0] + text_size[1]) / 2 - coordinate_y_adjustment
                            text_x = int(text_x)
                            text_y = int(text_y)
                            cv.putText(img, certi_name,
                                       (text_x, text_y),
                                       font,
                                       font_size,
                                       font_color, 10)
                            # for topic
                            text_x = (img.shape[1] - text_size[0]) / 2 + topic_x
                            text_y = (img.shape[0] + text_size[1]) / 2 - topic_y
                            text_x = int(text_x)
                            text_y = int(text_y)
                            cv.putText(img, certi_topic,
                                       (text_x, text_y),
                                       font,
                                       2,
                                       font_color, 10)

                            text_x = (img.shape[1] - text_size[0]) / 2 + date_x
                            text_y = (img.shape[0] + text_size[1]) / 2 - date_y
                            text_x = int(text_x)
                            text_y = int(text_y)
                            cv.putText(img, certi_date,
                                       (text_x, text_y),
                                       font,
                                       2,
                                       font_color, 10)
                            certi_path = output_path + user_contact.user_id.user_id.first_name + '.png'
                            rough = 'certificates/' + user_contact.user_id.user_id.first_name + '.png'
                            cv.imwrite(certi_path, img)

                            certificate = certi_path

                            print(certificate)
                            # data = Certificate.objects.get(user_id_id=user_contact.pk)
                            # data.delete()
                            credential = random.randint(125, 955842) * 10
                            data = Certificate(user_id_id=user_contact.pk, name=certi_name, certi_topic=certi_topic,
                                               issue_date=certi_date, email=user.email, certi_img=rough,
                                               serial_key=credential,certi_choose=2)
                            data.save()

                            messages.success(request, "Certificate Generated")
                            return redirect(request.path_info)

                    return render(request, 'virtualmain_pages/user-profile.html', context)

                return render(request, "virtualmain_pages/user-profile.html", context)

            return render(request,"virtualmain_pages/user-profile.html",context)


        context = {
            'user_data' : user_details,
            'reference': reference,
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
                    bio=request.POST['bio']
                    data = UserContact.objects.get(user_id_id=user_detail.pk)
                    data.address1 = address1
                    data.address2 = address2
                    data.gender = gender
                    data.user_bio=bio
                    data.save()
                    messages.success(request,"Updated Contact Info")
                    return redirect('userprofileEdit')

                else:
                    address1 = request.POST['address1']
                    address2 = request.POST['address2']
                    gender = request.POST['gender']
                    bio=request.POST['bio']

                    data = UserContact(address1=address1,address2=address2,gender=gender,user_bio=bio,user_id_id=user_detail.pk)
                    data.save()
                    messages.success(request,"Contact Info added")
                    return redirect(userEdit)
            if 'photo' in request.POST:
                try:
                    data = UserContact.objects.get(user_id_id=user_detail.pk)
                    if data.user_pic:
                        pic = request.FILES.get('user-profile-photo')
                        certi_create=request.POST['certi_create']
                        certi=Certificate(certi_img=pic,certi_topic=certi_create)
                        certi.save()
                        print(pic)
                        print("hai")
                        data.user_pic = pic
                        data.save()
                        messages.success(request,"Profile pic updated")
                    else:
                        pic = request.FILES.get('user-profile-photo')
                        certi_create=request.POST['certi_create']
                        data.user_pic = pic
                        data.save()
                        certi=Certificate(certi_img=pic,certi_topic=certi_create)
                        certi.save()
                        messages.success(request, "Profile pic added")
                except:
                    messages.error(request,"Complete your contact info to change Pic")
                    return redirect("userprofileEdit")


            if 'skill' in request.POST:
                type=request.POST['type']
                skills=request.POST['skills']

                create=UserSkill(user_id_id=user_detail.pk,category=type,skill=skills)
                create.save()
                messages.success(request, "Skills Added")

                return redirect(request.path_info)

            if 'tech_del' in request.POST:
                type=request.POST['type']
                skill=request.POST['skill1']

                find=UserSkill.objects.filter(user_id_id=user_detail.pk,category=type,skill=skill) #previously get()
                find.delete()
                messages.success(request,"Technical Skill Deleted")
                return redirect(request.path_info)

            if 'man_del' in request.POST:
                type=request.POST['type']
                skill=request.POST['skill2']

                find=UserSkill.objects.filter(user_id_id=user_detail.pk,category=type,skill=skill)
                find.delete()
                messages.success(request,"Management Skill Deleted")
                return redirect(request.path_info)

            if 'lan_del' in request.POST:
                type=request.POST['type']
                skill=request.POST['skill3']

                find=UserSkill.objects.filter(user_id_id=user_detail.pk,category=type,skill=skill)
                find.delete()
                messages.success(request,"Language Deleted")
                return redirect(request.path_info)



            if 'education' in request.POST:
                institution=request.POST['institution']
                start_month=request.POST['start-month']
                start_year=request.POST['start-year']
                end_month=request.POST['end-month']
                end_year=request.POST['end-year']
                degree=request.POST['degree']
                special=request.POST['special']
                gpa=request.POST['gpa']
                state=request.POST['state']

                edu=UserEducation(user_id_id=user_detail.pk,institution=institution,start_month=start_month,start_year=start_year,end_month=end_month,end_year=end_year,state=state,degree=degree,specialization=special,gpa=gpa)
                edu.save()
                messages.success(request, "Updated Education Info")
                return redirect(request.path_info)


            if 'work' in request.POST:
                role=request.POST['role']
                start_month=request.POST['start-month']
                start_year=request.POST['start-year']
                end_month=request.POST['end-month']
                end_year=request.POST['end-year']
                company=request.POST['company']
                state=request.POST['state']

                work=UserWorkExperience(user_id_id=user_detail.pk,job_role=role,start_month=start_month,start_year=start_year,end_month=end_month,end_year=end_year,state=state,company=company)
                work.save()

                messages.success(request, "Work Experience Added")
                return redirect(request.path_info)


            if 'edu_del' in request.POST:
                deg=request.POST['deg']
                spec=request.POST['spec']
                ins=request.POST['ins']

                find=UserEducation.objects.get(user_id_id=user_detail.pk,degree=deg,specialization=spec,institution=ins)
                find.delete()

                messages.success(request,"Educational Details Deleted")
                return redirect(request.path_info)

            if 'work_del' in request.POST:
                role=request.POST['role']
                com=request.POST['com']
                sm=request.POST['sm']
                sy=request.POST['sy']

                find=UserWorkExperience.objects.get(user_id_id=user_detail.pk,job_role=role,company=com,start_month=sm,start_year=sy)
                find.delete()

                messages.success(request,"Work Experience Deleted")
                return redirect(request.path_info)


        if UserContact.objects.filter(user_id_id=user_detail.pk).exists():

            users = UserContact.objects.order_by("gender")

            context ={
                'user_detail' : user_detail,
                'users' : users,


            }

            try:
                work=UserWorkExperience.objects.filter(user_id_id=user_detail.pk).order_by("-start_year")
            except:
                work=[]

            try:
                tech_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Technical')
            except:
                tech_skills=[]

            try:
                man_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Management')
            except:
                man_skills=[]

            try:
                lan_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Languages')
            except:
                lan_skills=[]


            if UserEducation.objects.filter(user_id_id=user_detail.pk).exists():

                try:
                    work=UserWorkExperience.objects.filter(user_id_id=user_detail.pk).order_by("-start_year")
                except:
                    work=[]

                try:
                    tech_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Technical')
                except:
                    tech_skills=[]

                try:
                    man_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Management')
                except:
                    man_skills=[]

                try:
                    lan_skills=UserSkill.objects.filter(user_id_id=user_detail.pk,category='Languages')
                except:
                    lan_skills=[]

                users = UserContact.objects.order_by("gender")
                education = UserEducation.objects.filter(user_id_id=user_detail.pk)
                context = {
                    'user_detail': user_detail,
                    'users': users,
                    'education': education,
                    'work':work,
                    'tech_skills':tech_skills,
                    'man_skills':man_skills,
                    'lan_skills':lan_skills

                }

                return render(request, 'virtualmain_pages/user-profile-edit.html', context)
            else:
                context ={
                    'work':work,
                    'tech_skills':tech_skills,
                    'man_skills':man_skills,
                    'lan_skills':lan_skills,
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
                'user_detail':user_detail,


            }
            idd =1
            return render(request,'virtualmain_pages/user-profile-edit.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def userProject(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user

        user_details = UserDetails.objects.get(user_id_id=user.pk)
        try:
            if StudentCFP.objects.filter(user_id_id=user_details.pk).exists():

                cfp_details = StudentCFP.objects.get(user_id_id=user_details.pk)
                #Displaying Projects
                projects1=ProjectManager.objects.filter(project_category=cfp_details.category_one)
                projects2=ProjectManager.objects.filter(project_category=cfp_details.category_two)

                cfp1_projects=[]
                cfp2_projects=[]

                for i in projects1:
                    res=i.project_cfp.find(cfp_details.role_one)
                    if res != -1:
                        cfp1_projects.append(i)

                for j in projects2:
                    res=j.project_cfp.find(cfp_details.role_two)
                    if res != -1:
                        cfp2_projects.append(j)


                enrolled_projects=EnrolledProject.objects.filter(user=user)

                print('suceess')

                # if ProgressCourse.objects.filter(user_id=user.pk).exists():
                #     print("hello")
                #     progress_course = ProgressCourse.objects.filter(user=user)
                #
                # else:
                #
                #     progress_course = None

                context = {
                    'cfp1_projects':cfp1_projects,
                    'cfp2_projects':cfp2_projects,
                    'enrolled_projects':enrolled_projects

                }
                return render(request, 'virtualmain_pages/user-project.html', context)
            else:
                return render(request,'virtualmain_pages/user-project.html')

        except:
            print("Error")

        return render(request,'virtualmain_pages/user-project.html', context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

@login_required
def userProjectDetails(request,id):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        p_id=id
        project=ProjectManager.objects.get(id=p_id)
        check=EnrolledProject.objects.filter(project=project).count()
        vacancy=project.candidates_required - check
        print(project.candidates_required)
        if request.method == 'POST':
            count=EnrolledProject.objects.filter(project=project).count()
            print(count)
            if count < project.candidates_required:
                try:
                    check=EnrolledProject.objects.filter(user=user,project=project).exists()
                    if check == True:
                        messages.error(request,"You have already enrolled in this course")
                        return redirect(request.path_info)
                    else:
                        data=EnrolledProject(user=user,project=project)
                        data.save()
                        messages.success(request,"You have sucessfully enrolled in this course")
                        return redirect(request.path_info)

                except:
                    print("Error")

                return redirect(request.path_info)

            else:
                messages.error(request,"There is no vacancy for this project")
                return redirect(request.path_info)

        context={
            'project':project,
            'vacancy':vacancy
        }

    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

    return render(request,'virtualmain_pages/user-project-details.html',context)



def userblogspage(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        blogs=BlogManager.objects.all()
        context={
            'blogs':blogs
        }

    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

    return render(request,'virtualmain_pages/user_blogs_page.html',context)

def userblogsdetail(request,id):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        bid=id
        blog=BlogManager.objects.get(id=bid)
        context={
            'blog':blog
        }

    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')

    return render(request,'virtualmain_pages/user_blog_detail.html',context)


@login_required
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

        if request.method == 'POST':
            if 'courseDelete' in request.POST:
                print("Delete Course")
                c_id = request.POST['del_id']
                try:
                    course_del =Course.objects.get(id = c_id).delete()
                    messages.success(request,"Deleted successfully")
                except:
                    messages.error(request,"Some error occured")


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
        inst=RoleDetail.objects.all()
        data=CreateCourse.objects.get(create_id=0)

        if request.method == "POST":
            title = request.POST["title"]
            instructor=request.POST["instructor"]
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


            create = Course(user_id=user.id,title=title,tagline=tagline,short_description=short_description,instructor=instructor,
                           course_image=image,category=category,role=role,course=course,difficulty_level=difficulty_level,meta_keywords=meta_keywords,
                            meta_description=meta_description,course_points=course_points,certificate=certificate,requirements=requirements,learnings=learnings)
            create.save()

            inst=RoleDetail.objects.all()


            obj=CreateCourse.objects.all()
            obj.delete()


            return redirect("/csmdashboard/")

        context={
            'data':data,
            'inst':inst
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
        t_id = datas.id
        print(t_id)
        if request.method == "POST":
            if 'course_submit' in request.POST:
                title = request.POST["title"]
                instructor=request.POST["instructor"]
                tagline  = request.POST["tagline"]
                short_description=request.POST["description"]
                course_image = request.FILES.get('course_image', None)
                # course_image = request.FILES['course_image']
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
                datas.instructor=instructor
                datas.tagline=tagline
                datas.short_description=short_description
                if course_image is not None:
                    datas.course_image=course_image
                    print(course_image)
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

        inst=RoleDetail.objects.all()
        context ={
            'datas' : datas,
            'req_list':req_list,
            'learn_list':learn_list,
            'inst':inst,
            't_id':t_id,
        }
        return render(request,'csm_pages/csm_edit_course.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('logout')


def testEdit(request,id):
    if request.method=='POST':
        if 'category' in request.POST:
            count=CreateCourse.objects.all().count()
            if count==0:
                cag=request.POST['category']
                data=CreateCourse(create_category=cag)
                data.save()
                return redirect(request.path_info)

            else:
                cag=request.POST['category']
                data=CreateCourse.objects.get(create_id=0)
                data.create_category=cag
                data.create_role=None
                data.save()
                return redirect(request.path_info)


        if 'role' in request.POST:
            c_course=request.POST['c_course']
            data=CreateCourse.objects.get(create_category=c_course)
            role=request.POST.get('role')
            data.create_role=role
            data.save()
            return redirect(request.path_info)

        if 'edit-course-submit' in request.POST:
            confirm_cag=request.POST['confirm_cag']
            confirm_role=request.POST['confirm_role']
            confirm_course=request.POST['confirm_course']

            # check=CFP_role.objects.get(cfp_role=confirm_role)
            # if check.cfp_category != confirm_cag:
            #     messages.error(request, 'The Category do not match with CFP Role')
            #     return redirect('/testEdit/')
            # else:
            data=CreateCourse.objects.get(create_role=confirm_role)
            data.create_course=confirm_course
            data.save()

            obj=Course.objects.get(id=id)
            obj.category=data.create_category
            obj.role=data.create_role
            obj.course=data.create_course
            obj.save()


            data=CreateCourse.objects.all().delete()

            messages.success(request,"Course Changes Successfull Created Check Database")
            return redirect('csmEditCourse',id)


    cag_data=CareerCategory.objects.all()
    if CreateCourse.objects.count()!=0:
        obj=CreateCourse.objects.get(create_id=0)
        role_list=CFP_role.objects.filter(cfp_category=obj.create_category)
        try:
            abc=CreateCourse.objects.get(create_id=0)
            role_text=abc.create_role
            role_split=role_text.split('+')
            abc=[]
            for i in role_split:
                course_text=CFP_role.objects.get(cfp_role=i)
                course=course_text.cfp_course.split('_')
                abc.append(course)

            common=set.intersection(*[set(list) for list in abc])
            course_list=list(common)
            # print(course_list)
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
        'course_list':course_list,
        'id':id
    }
    return render(request,'csm_pages/testEdit.html',context)


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
                if Lesson.objects.filter(lesson_id_id=c_id,lesson_name=lesson_name).exists():
                    messages.error(request,"Lesson name already exists")
                    return redirect('csmAddCurriculam',id)
                less_private = random.randint(112,1000)*100
                Less = Lesson(lesson_name=lesson_name,lesson_private=less_private,lesson_id_id=c_id)
                Less.save()
                messages.success(request,"Lesson Added")
                print("success")

            if 'addTopic' in request.POST:
                topic_caption = request.POST['topic_descrip']
                topic_video = request.POST['topic_video']
                lesson = request.POST['les_id']



                try:
                    lesson_private = Lesson.objects.get(lesson_private=lesson)
                    if lesson_private:
                        print("enter")
                        if Lesson_Topic.objects.filter(topic_id_id=lesson_private.pk,topic_caption=topic_caption).exists():
                            messages.error(request,"Topic name already exists")
                            return redirect('csmAddCurriculam',id)
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
                video = request.POST['topic_video']
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

@login_required
def csmSettings(request):
    if request.user.is_active and request.user.is_staff and not request.user.is_superuser:
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
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')


# TL MODULE SECTION
@login_required
def tlDashboard(request):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:
        user=request.user
        print(user)
        data=RoleDetail.objects.get(role_user_email=user.email)
        projects=ProjectManager.objects.filter(project_tl=data.role_user_id)
        completed_projects=ProjectManager.objects.filter(project_tl=data.role_user_id,project_status='Completed')
        context={
            'projects':projects,
            'completed_projects':completed_projects
        }
        return render(request,'TL_Pages/tl_dashboard.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')

@login_required
def tlProjectDetails(request,id):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:
        data=ProjectManager.objects.get(id=id)
        students=EnrolledProject.objects.filter(project=data)
        info=UserDetails.objects.all()
        context={
            'data':data,
            'students':students,
            'info' : info,
        }
        return render(request,'TL_Pages/tl_project_details.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')



@login_required
def tlProjectStudentDetails(request,pid,id):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:
        print("hai",request.user.pk)

        student=User.objects.get(id=id)
        userdetails = UserDetails.objects.get(user_id_id=student.pk)

        user_contact = UserContact.objects.get(user_id_id=userdetails.pk)
        user_education = UserEducation.objects.filter(user_id_id=userdetails.pk)
        pdata = ProjectManager.objects.get(id = pid)
        if request.method == 'POST':
            if 'reward' in request.POST:
                points = request.POST['points']
                role = request.POST['role']
                if ProjectPoint.objects.filter(user_id_id=userdetails.pk,proj_role=role).exists():
                    data = ProjectPoint.objects.get(user_id_id=userdetails.pk,proj_role=role)
                    point = int(data.proj_points) + int(points)
                    if point >999:
                        messages.error(request,"User reached maximum points")
                        return redirect('tlProjectStudentDetails',pid,id)
                    data.proj_points = point
                    data.save()
                    messages.success(request,"Rewards added")
                else:
                    data = ProjectPoint(proj_points=points,user_id_id=userdetails.pk,proj_role=role)
                    data.save()
                    messages.success(request,"First reward added")

        try:
            cfp_details = StudentCFP.objects.get(user_id_id=userdetails.pk)
            if StudentCFP.objects.filter(user_id_id=userdetails.pk,role_one=pdata.project_cfp).exists():
                cfp_details = cfp_details.role_one
            elif StudentCFP.objects.filter(user_id_id=userdetails.pk,role_two=pdata.project_cfp).exists():
                cfp_details = cfp_details.role_two
            else:
                cfp_details=None

        except:
            cfp_details = None

        tags = CourseTag.objects.filter(user_id_id=userdetails.pk,course_role=cfp_details)



        # For Displaying Progress Bar
        # claim = Claim.objects.all()


        try:
            claim = Claim.objects.filter(user_id = userdetails.pk)

        except:
            claim =None

        context={
            'user_contact':user_contact,
            'user_education':user_education,
            'student':student,
            'user_data':userdetails,
            'cfp_details':cfp_details,
            'claim':claim,
            'tags':tags,
        }
        return render(request,'TL_Pages/tl_project_student_details.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')



@login_required
def tlSettings(request):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:
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
                    return redirect(tlSettings)
            except:
                messages.error(request, 'User is not able to change password !')

            else:
                messages.error(request,'Password not matching !')
                return redirect(tlSettings)
        context = {
            'form': form,
        }
        return render(request, "TL_Pages/tl_settings.html", context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')

# PROJECT MODULE SECTION

@login_required
def projectManager(request):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:

        cfp_list=CFP_role.objects.all()
        user = request.user
        if request.method=='POST':
            if 'category' in request.POST:
                count=ProjectCFPStore.objects.all().count()
                if count==0:
                    cag=request.POST['category']
                    data=ProjectCFPStore(create_category=cag)
                    data.save()
                    return redirect('/projectmanager/')

                else:
                    cag=request.POST['category']
                    data=ProjectCFPStore.objects.get(create_id=0)
                    data.create_category=cag
                    data.create_role=None
                    data.save()
                    return redirect('/projectmanager/')


            if 'role' in request.POST:
                c_course=request.POST['c_course']
                data=ProjectCFPStore.objects.get(create_category=c_course)
                ch=request.POST.getlist('project_cfp')
                role=""
                for i in ch:
                    role+=i
                    role+="+"
                role_str=role[:-1]

                data.create_role=role_str
                data.save()
                return redirect('/projectmanager/')


            if 'project_submit' in request.POST:
                project_title=request.POST["project_title"]
                project_description=request.POST["project_description"]
                project_thumbnail=request.FILES.get("project_thumbnail")
                project_duration=request.POST["project_duration"]
                candidates_required=request.POST["candidates_required"]
                project_docs=request.FILES.get("project_docs")
                project_category=request.POST.get("project_category")
                project_cfp=request.POST.get("project_role")
                project_status=request.POST["progress"]


                proj=ProjectManager.objects.create(
                    user_id= user.pk,
                    project_title=project_title,
                    project_description=project_description,
                    project_thumbnail=project_thumbnail,
                    project_duration=project_duration,
                    candidates_required=candidates_required,
                    project_docs=project_docs,
                    project_category=project_category,
                    project_cfp=project_cfp,
                    project_status=project_status
                )
                # proj.project_cfp.set(cfp_list)
                proj.save()

                obj=ProjectCFPStore.objects.all().delete()
                return redirect("/projectdashboard/")


        cag_data=CareerCategory.objects.all()
        if ProjectCFPStore.objects.count()!=0:
            obj=ProjectCFPStore.objects.get(create_id=0)
            role_list=CFP_role.objects.filter(cfp_category=obj.create_category)
            ch=obj.create_role
            if ch==None:
                cfp_list=[]
            else:
                cfp_list=ch.split('+')

        else:
            obj="Choose"
            role_list=[]
            cfp_list=[]

        context={
            'cag_data':cag_data,
            'obj':obj,
            'role_list':role_list,
            'cfp_list':cfp_list
        }


        return render(request,'ProjectModule_Pages/Project_manager.html',context)
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')


@login_required
def projectEditManager(request,id):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:
        pid=id
        project=ProjectManager.objects.get(id=pid)
        check=ProjectCFPStore.objects.all().count
        cfp_list=CFP_role.objects.all()
        tls=RoleDetail.objects.filter(user_role="TL")
        if request.method=='POST':
            if 'tl' in request.POST:
                tl=request.POST['tl']
                project.project_tl=tl
                project.save()
                return redirect(request.path_info)


            if 'category' in request.POST:
                count=ProjectCFPStore.objects.all().count()
                if count==0:
                    cag=request.POST['category']
                    data=ProjectCFPStore(create_category=cag)
                    data.save()
                    return redirect(request.path_info)

                else:
                    cag=request.POST['category']
                    data=ProjectCFPStore.objects.get(create_id=0)
                    data.create_category=cag
                    data.create_role=None
                    data.save()
                    return redirect(request.path_info)


            if 'role' in request.POST:
                c_course=request.POST['c_course']
                data=ProjectCFPStore.objects.get(create_category=c_course)
                ch=request.POST.getlist('project_cfp')
                role=""
                for i in ch:
                    role+=i
                    role+="+"
                role_str=role[:-1]

                data.create_role=role_str
                data.save()
                return redirect(request.path_info)


            if 'change_project_submit' in request.POST:
                project_title=request.POST["project_title"]
                project_description=request.POST["project_description"]
                project_thumbnail=request.FILES.get("project_thumbnail")
                project_duration=request.POST["project_duration"]
                candidates_required=request.POST["candidates_required"]
                project_docs=request.FILES.get("project_docs")
                project_category=request.POST.get("project_category")
                project_cfp=request.POST.get("project_role")
                project_status=request.POST["progress"]


                project.project_title=project_title
                project.project_description=project_description
                project.project_thumbnail=project_thumbnail
                project.project_duration=project_duration
                project.candidates_required=candidates_required
                project.project_docs=project_docs
                project.project_category=project_category
                project.project_cfp=project_cfp
                project.project_status=project_status


                project.save()

                obj=ProjectCFPStore.objects.all().delete()
                return redirect("/projectdashboard/")


            if 'del-project' in request.POST:
                find=ProjectManager.objects.get(id=pid)
                find.delete()
                # messages.success(request,'Project Successfully Deleted')
                return redirect('projectDashboard')

        cag_data=CareerCategory.objects.all()
        if ProjectCFPStore.objects.count()!=0:
            obj=ProjectCFPStore.objects.get(create_id=0)
            role_list=CFP_role.objects.filter(cfp_category=obj.create_category)
            ch=obj.create_role
            if ch==None:
                cfp_list=[]
            else:
                cfp_list=ch.split('+')

        else:
            obj="Choose"
            role_list=[]
            cfp_list=[]

        context={
            'cag_data':cag_data,
            'obj':obj,
            'role_list':role_list,
            'cfp_list':cfp_list,
            'project':project,
            'check':check,
            'tls':tls
        }

        return render(request,'ProjectModule_Pages/Project_edit_manager.html',context)
    else:
        messages.error(request, 'Wrong URL')
        return redirect('login')

@login_required
def projectDashboard(request):
    if request.user.is_active and request.user.is_superuser and not request.user.is_staff:
        projects=ProjectManager.objects.all()
        context={
            'projects':projects,
        }
        return render(request,'ProjectModule_Pages/Project_dashboard.html',context)
    else:
        messages.error(request,'Wrong URL')
        return redirect('login')

@login_required
def pcmSettings(request):

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
                return redirect(pcmSettings)
        except:
            messages.error(request, 'User is not able to change password !')

        else:
            messages.error(request,'Password not matching !')
            return redirect(pcmSettings)
    context = {
        'form': form,
    }
    return render(request, "ProjectModule_Pages/pcm_settings.html", context)



def insDashboard(request):
    if request.user.is_active:
        user=request.user
        try:
            role = RoleDetail.objects.get(user_id_id=user.pk)
            if role.user_role == "Instructor":
                assign_courses=Course.objects.filter(instructor=user.email)

                context={
                    'assign_courses':assign_courses
                }
                return render(request,'Instructor_pages/Instructor_dashboard.html',context)
            else:
                messages.error(request,"Wrong credentials")
                return redirect('login')
        except:
            messages.error(request,"Wrong credentials")
            return redirect('login')

    else:
        messages.error(request,"Wrong")
        return redirect('login')


@login_required
def insCourseInfo(request,id):
    if request.user.is_active:
        cid=id
        info=Course.objects.get(id=cid)
        context={
            'info':info
        }
        return render(request,"Instructor_pages/Ins_Course_info.html",context)

    else:
        messages.error(request,'Wrong URL')
        return redirect('login')

    return render(request,"Instructor_pages/Ins_Course_info.html",context)





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

            return redirect('cfp_create')

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

    return render(request,'Admin_pages/cfp_edit.html',context)


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
            return redirect('cfp_create')

    context={
        'datas':datas,
    }
    return render(request,'Admin_pages/category_edit.html',context)




def createcourse(request):
    if request.method=='POST':
        if 'category' in request.POST:
            count=CreateCourse.objects.all().count()
            if count==0:
                cag=request.POST['category']
                data=CreateCourse(create_category=cag)
                data.save()
                return redirect('/createcourse/')

            else:
                cag=request.POST['category']
                data=CreateCourse.objects.get(create_id=0)
                data.create_category=cag
                data.create_role=None
                data.save()
                return redirect('/createcourse/')


        if 'role' in request.POST:
            c_course=request.POST['c_course']
            # role=request.POST['role']
            data=CreateCourse.objects.get(create_category=c_course)
            # data.create_role=role
            # data.save()
            role=request.POST.get('role')  #previously roles[]
            # role=""
            # for i in ch:
            #     role+=i
            #     role+="+"
            # role_str=role[:-1]

            data.create_role=role
            data.save()
            return redirect('/createcourse/')

        if 'course-submit' in request.POST:
            confirm_cag=request.POST['confirm_cag']
            confirm_role=request.POST['confirm_role']
            confirm_course=request.POST['confirm_course']

            # check=CFP_role.objects.get(cfp_role=confirm_role)
            # if check.cfp_category != confirm_cag:
            #     messages.error(request, 'The Category do not match with CFP Role')
            #     return redirect('/test/')
            # else:
            data=CreateCourse.objects.get(create_role=confirm_role)
            data.create_course=confirm_course
            data.save()
            messages.success(request,"Course Successfully Created Check Database")
            return redirect('/csmaddcourse/')


    cag_data=CareerCategory.objects.all()
    if CreateCourse.objects.count()!=0:
        obj=CreateCourse.objects.get(create_id=0)
        role_list=CFP_role.objects.filter(cfp_category=obj.create_category)
        try:
            abc=CreateCourse.objects.get(create_id=0)
            role_text=abc.create_role
            role_split=role_text.split('+')
            abc=[]
            for i in role_split:
                course_text=CFP_role.objects.get(cfp_role=i)
                course=course_text.cfp_course.split('_')
                abc.append(course)

            # course_list=[ele[0] for ele in zip(*abc) if len(set(ele)) == 1]
            common=set.intersection(*[set(list) for list in abc])
            course_list=list(common)
            # print(course_list)
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

#  Career choice

# def careerchoice(request):
#     user = request.user
#     details = UserDetails.objects.get(user_id_id=user.pk)
#
#     if request.method=='POST':
#         if 'first-category' in request.POST:
#             count=CareerChoice.objects.all().count()
#             if count==0:
#
#                 category=request.POST['first-category']
#                 data=CareerChoice(career_id=1,first_choice_category=category)
#                 data.save()
#                 return redirect('careerchoice')
#
#             else:
#                 print("hai")
#                 cag=request.POST['first-category']
#                 data=CareerChoice.objects.get(career_id=1)
#                 data.first_choice_category=cag;
#                 data.first_choice_role=None
#                 data.save()
#                 return redirect('careerchoice')
#
#
#         if 'first-role' in request.POST:
#             con_cag=request.POST['con_cag']
#             role=request.POST['first-role']
#             compare=CFP_role.objects.get(cfp_role=role)
#             if compare.cfp_category == con_cag:
#                 data=CareerChoice.objects.get(career_id=1)
#                 data.first_choice_role=role
#                 data.save()
#                 return redirect('careerchoice')
#             else:
#                 messages.error(request,"Role and Category Do not Match")
#                 return redirect('careerchoice')
#
#
#
#
#         if 'second-category' in request.POST:
#             count=CareerChoice.objects.all().count()
#             if count==0:
#                 category=request.POST['second-category']
#                 data=CareerChoice(career_id=1,second_choice_category=category)
#                 data.save()
#                 return redirect('/careerchoice/')
#
#             else:
#                 cag=request.POST['second-category']
#                 data=CareerChoice.objects.get(career_id=1)
#                 data.second_choice_category=cag
#                 data.second_choice_role=None
#                 data.save()
#                 return redirect('/careerchoice/')
#
#
#         if 'second-role' in request.POST:
#             con_cag=request.POST['con_cag']
#             role=request.POST['second-role']
#             compare=CFP_role.objects.get(cfp_role=role)
#             if compare.cfp_category == con_cag:
#                 data=CareerChoice.objects.get(second_choice_category=con_cag)
#                 data.second_choice_role=role
#                 data.save()
#                 return redirect('careerchoice')
#             else:
#                 # messages.error(request,"Role and Category Do not Match")
#                 return redirect('careerchoice')
#
#
#
#         if 'confirm_submit' in request.POST:
#             confirm_first_category=request.POST['confirm_first_category']
#             confirm_first_role=request.POST['confirm_first_role']
#             confirm_second_category=request.POST['confirm_second_category']
#             confirm_second_role=request.POST['confirm_second_category']
#             data=StudentCFP(category_one=confirm_first_category,role_one=confirm_first_role,category_two=confirm_second_category,role_two=confirm_second_role,user_id_id=details.pk)
#             data.save()
#             messages.success(request,"CFP Created")
#             return redirect('userprofileEdit')
#
#     cag_list=CareerCategory.objects.all()
#     if CareerChoice.objects.count()!=0:
#         obj=CareerChoice.objects.get(career_id=1)
#         role_list_one=CFP_role.objects.filter(cfp_category=obj.first_choice_category)
#         role_list_two=CFP_role.objects.filter(cfp_category=obj.second_choice_category)
#
#     else:
#         obj="Choose"
#         role_list_one=[]
#         role_list_two=[]
#
#     context={
#         'cag_list':cag_list,
#         'obj':obj,
#         'role_list_one':role_list_one,
#         'role_list_two':role_list_two
#     }
#     return render(request,'virtualmain_pages/careerchoice.html',context)

def UserCfp(request):
    user = request.user
    details = UserDetails.objects.get(user_id_id=user.pk)

    if request.method=='POST':
        if 'first-category' in request.POST:
            count=CareerChoice.objects.all().count()
            if count==0:
                category=request.POST['first-category']
                data=CareerChoice(career_id=1,first_choice_category=category)
                data.save()
                return redirect('usercfp')

            else:
                cag=request.POST['first-category']
                data=CareerChoice.objects.get(career_id=1)
                data.first_choice_category=cag
                data.first_choice_role=None
                data.save()
                return redirect('usercfp')


        if 'first-role' in request.POST:
            con_cag=request.POST['con_cag']
            role=request.POST['first-role']
            compare=CFP_role.objects.get(cfp_role=role)
            if compare.cfp_category == con_cag:
                data=CareerChoice.objects.get(career_id=1)
                data.first_choice_role=role
                data.save()
                messages.success(request,"First Choice submitted")
                return redirect('usercfp')
            else:
                messages.error(request,"Role and Category Do not Match")
                return redirect('usercfp')




        if 'second-category' in request.POST:
            count=CareerChoice.objects.all().count()
            if count==0:
                category=request.POST['second-category']
                data=CareerChoice(career_id=1,second_choice_category=category)
                data.save()
                return redirect('usercfp')

            else:
                cag=request.POST['second-category']
                data=CareerChoice.objects.get(career_id=1)
                data.second_choice_category=cag
                data.second_choice_role=None
                data.save()
                return redirect('usercfp')


        if 'second-role' in request.POST:

            con_cag=request.POST['con_cag']
            role=request.POST['second-role']
            compare=CFP_role.objects.get(cfp_role=role)
            if compare.cfp_category == con_cag:
                data=CareerChoice.objects.get(second_choice_category=con_cag)
                data.second_choice_role=role
                data.save()

                return redirect('usercfp')
            else:
                # messages.error(request,"Role and Category Do not Match")
                return redirect('usercfp')



        if 'confirm_submit' in request.POST:
            try:
                if StudentCFP.objects.filter(user_id_id=details.pk).exists():
                    messages.error(request,"CFP Choosed already")
                    return redirect('usercfp')
                compare_role = CareerChoice.objects.get()
                print(compare_role.first_choice_role)
                if compare_role.first_choice_role == compare_role.second_choice_role:
                    print("same")
                    messages.error(request, "First choice and Second choice are same")
                    return redirect('usercfp')
            except:
                messages.error(request,"Some Error Occured")
                return redirect('usercfp')
            confirm_first_category=request.POST['confirm_first_category']
            confirm_first_role=request.POST['confirm_first_role']
            confirm_second_category=request.POST['confirm_second_category']
            confirm_second_role=request.POST['confirm_second_role']
            data=StudentCFP(category_one=confirm_first_category,role_one=confirm_first_role,category_two=confirm_second_category,role_two=confirm_second_role,user_id_id=details.pk)
            data.save()
            find=CareerChoice.objects.all().delete()
            messages.success(request,"CFP Created")
            return redirect('userprofileEdit')
    cag_list = CareerCategory.objects.all()
    if CareerChoice.objects.count() != 0:
        obj = CareerChoice.objects.get(career_id=1)
        role_list_one = CFP_role.objects.filter(cfp_category=obj.first_choice_category)
        role_list_two = CFP_role.objects.filter(cfp_category=obj.second_choice_category)

    else:
        obj = "Choose"
        role_list_one = []
        role_list_two = []

    context = {
        'cag_list': cag_list,
        'obj': obj,
        'role_list_one': role_list_one,
        'role_list_two': role_list_two
    }
    return render(request,'virtualmain_pages/user-cfp.html',context)


#Blog user
@login_required
def blogManager(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user=request.user
        if request.method=='POST':
            if 'blog_submit' in request.POST:
                blog_title=request.POST["blog_title"]
                blog_body=request.POST["blog_body"]
                blog_thumbnail=request.FILES.get("blog_thumbnail")
                blog_category=request.POST["category"]


                blog=BlogManager.objects.create(
                    user_id= user.id,
                    blog_title=blog_title,
                    blog_body=blog_body,
                    blog_thumbnail=blog_thumbnail,
                    blog_category=blog_category,
                )
                # proj.project_cfp.set(cfp_list)
                blog.save()
                return redirect("/blogdashboard/")
        cag_data=BlogCategory.objects.all()
        context={
            'cag_data':cag_data,
        }

        return render(request,'blog_pages/blog_manager.html',context)

    else:
        messages.error(request,"Wrong url")
        return redirect('login')

@login_required
def blogEditManager(request,id):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user=request.user
        pid=id
        data=BlogManager.objects.get(id=pid)
        cag_data=BlogCategory.objects.all()
        if request.method=='POST':
            if 'blog_edit' in request.POST:
                blog_title=request.POST["blog_title"]
                blog_body=request.POST["blog_body"]
                blog_thumbnail=request.FILES.get("blog_thumbnail")
                blog_category=request.POST["category"]

                data.blog_title=blog_title
                data.blog_body=blog_body
                data.blog_thumbnail=blog_thumbnail
                data.blog_category=blog_category
                data.save()
                return redirect('/blogDashboard/')

        context={
            'data':data,
            'cag_data':cag_data
        }

        return render(request,'blog_pages/blog_edit_manager.html',context)
    else:
        messages.error(request,"Wrong url")
        return redirect('login')


@login_required
def blogDashboard(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user=request.user
        blogs=BlogManager.objects.filter(user=user.pk)
        context={
            'blogs':blogs,

        }
        return render(request,'blog_pages/blog_dashboard.html',context)
    else:
        messages.error(request,"Wrong url")
        return redirect('login')


def blogcategorycreate(request):
    if request.method=='POST':
        if 'category_submit' in request.POST:
            cag_name=request.POST['cagname']

            if BlogCategory.objects.filter(blog_category=cag_name).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')

            if BlogCategory.objects.filter(blog_category=cag_name.upper()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')

            if BlogCategory.objects.filter(blog_category=cag_name.lower()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')

            if BlogCategory.objects.filter(blog_category=cag_name.capitalize()).exists():
                messages.error(request, 'The Category already exists')
                return redirect('blogcategorycreate')


            category_id=BlogCategory.objects.all().count()+1
            cag_obj=BlogCategory(blog_category_id=category_id,blog_category=cag_name)
            cag_obj.save()
            messages.success(request, 'New Category created')

            return redirect('blogcategorycreate')

    return render(request,'blog_pages/blog_create_category.html')




def pricing(request):
    return render(request,"virtualmain_pages/pricing.html")


def payment(request):
    print("payment page")
    user_id = request.user.pk
    refernces = Reference.objects.all()
    original_price = 15254
    first = 5900
    print(user_id)
    if request.method == "POST":
        if 'ref' in request.POST:
            ref = request.POST['reference']
            try:
                if Reference.objects.filter(ref_id=ref).exists():

                    if not Reference.objects.filter(used_id=user_id).exists():
                        ref_detail = Reference.objects.get(ref_id=ref)
                        print(ref_detail.used_peoples)
                        ref_detail.used_peoples = 1
                        ref_detail.used_id = user_id
                        ref_detail.save()
                        messages.success(request, "Reference Applied")
                    else:
                        messages.error(request,"Reference Key Already Applied")
                    off_amt = (original_price * 10 ) / 100
                    base_amt = original_price - off_amt
                    gst_amt = (base_amt * 18) /100
                    total_amt = base_amt+gst_amt

                    context ={
                        'base_amt':base_amt,
                        'total_amt':total_amt
                    }

                    return render(request,"payment/payment_page.html",context)
                else:
                    print("Not exists")
                    messages.error(request,"Reference ID Invalid")
            except:
                messages.error(request,"Reference key error")
        if 'emi' in request.POST:
            print(first)
            total = request.POST['total']
            remain= float(total) - float(first)
            install_3 = (remain / 3) +99
            install_3 = round(install_3)
            install_5 = (remain / 5) + 99
            install_5 = round(install_5)
            context = {
                'total' : total,
                'first' : first,
                'install_3' : install_3,
                'install_5' : install_5,
            }

            return render(request, 'payment/payment_page.html', context)
    gst_amt2 = (original_price * 18 )/100
    total_amt2 = original_price + gst_amt2
    context={
        'total_amt' :total_amt2
    }
    return render(request,'payment/payment_page.html',context)


def error_404_view(request, exception):
    return render(request, 'virtualmain_pages/404.html')
def error_500_view(request):
    return render(request, 'virtualmain_pages/500.html')
