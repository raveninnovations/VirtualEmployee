import re
import random, math
import uuid
import datetime as dt
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth import login,logout,authenticate
from django.contrib import auth
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from moviepy.editor import VideoFileClip
# EMAIL FROM SETTINGS
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from VirtualMain.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage

from datetime import datetime
from .forms import (AddUserForm)

from .models import UserDetails, RoleDetail, Course, Lesson, Lesson_Topic, CareerCategory, CFP_role,ProjectManager,AdminLicense,UserContact,UserEducation,CreateCourse,CareerChoice,StudentCFP,ProjectCFPStore,ProgressCourse,UsedLicense


# Create your views here.
# ADMIN SECTION

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

                OTP = random.randint(99, 9999)
                request.session['num'] = OTP
                print(OTP)
                mail_subject = "OTP for Admin License Page"
                message = f'Hi,{request.user.first_name} is requesting for an OTP to access Admin License page, please share this OTP : {OTP}'
                email = EmailMessage(mail_subject, message, from_email=EMAIL_HOST_USER, to=[user_email,])
                email.send()

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
        return render(request,'Admin_pages/courses.html')
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
                messages.success(request,"Email has been sent successfully")
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

            context ={
                'student':student_info,
                'license':license_info
            }
            return render(request,'Admin_pages/admin_license_info.html',context)

        except:
            print("error")

        return render(request,'Admin_pages/admin_license_info.html')
    else:
        messages.error(request,"Wrong URL")
        return redirect('login')

def adduser(request):
    form = AddUserForm
    lisences = AdminLicense.objects.all()
    if request.method =='POST':
        firstname = request.POST['first']
        lastname = request.POST['last']
        userphone = request.POST['user_phone']
        email = request.POST['email']
        username = request.POST['email']
        password = request.POST['password1']
        conform = request.POST['password2']
        license_key = request.POST['license']

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
                        key.delete()
                        messages.success(request,"License Key applied ! You can login")

                else:
                    messages.error(request,'License Key Not Valid')
                    return redirect('register')
            else:
                license_key =None
            User.objects.create_user(username=username,email=email,first_name=firstname,last_name=lastname,password=password)
            u_id = User.objects.get(username=username)
            addusr = UserDetails(user_id=u_id,user_pass=password,user_phone=userphone,user_unique=unique_id,user_license=license_key)
            addusr.save()
            if license_key:

                return redirect('login')
            else:
                return redirect('pricing')

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
        user = request.user

        user_details = UserDetails.objects.get(user_id_id=user.pk)
        course_data = Course.objects.all()

        try:
            if StudentCFP.objects.filter(user_id_id=user_details.pk).exists():

                cfp_details = StudentCFP.objects.get(user_id_id=user_details.pk)

                # CFP  COURSES
                lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)

                lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)

                if ProgressCourse.objects.filter(user=user).exists():
                    print("hai")
                    progress_course = ProgressCourse.objects.filter(user=user)
                else:

                    progress_course = None

                context = {
                    'cfp_details':cfp_details,
                    'lists':lists,
                    'lists2':lists2,
                    'course_data': course_data,
                    'progress_course':progress_course

                }
                return render(request,'virtualmain_pages/dashboard.html',context)
        except:
            print("Error")

        context={
            'course_data':course_data,

        }
        return render(request,'virtualmain_pages/dashboard.html',context)
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
        user = request.user
        course_details = Course.objects.get(id = id)
        print(course_details.pk)
        lessons = Lesson.objects.filter(lesson_id_id=course_details.pk)
        topics = Lesson_Topic.objects.all()

        if request.method=='POST':
            try:
                if ProgressCourse.objects.get(user=user,course_id=id).exists():
                    return redirect(request.path_info)
                # else:
                #     obj=ProgressCourse(user=user,course_id=id,title=course_details.title,role=course_details.role,course=course_details.course)
                #     return redirect(request.path_info)
            except:
                obj=ProgressCourse(user=user,course_id=id,title=course_details.title,category=course_details.category,role=course_details.role,course=course_details.course,course_image=course_details.course_image)
                obj.save()
                return redirect(request.path_info)
            return redirect(request.path_info)

        context ={
            'course_details':course_details,
            'lessons': lessons,
            'topics': topics,
        }

    return render(request,'virtualmain_pages/user_course_lesson.html',context)

@login_required
def userprofile(request):
    if request.user.is_active and not request.user.is_staff and not request.user.is_superuser:
        user = request.user
        print(user.id)
        user_details = UserDetails.objects.get(user_id_id=user.pk)
        courses = Course.objects.all()

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
                # CFP
                if StudentCFP.objects.filter(user_id_id=user_details.pk).exists():
                    cfp_details = StudentCFP.objects.get(user_id_id=user_details.pk)
                    # CFP  COURSES
                    lists = Course.objects.filter(category=cfp_details.category_one, role=cfp_details.role_one)
                    lists2 = Course.objects.filter(category=cfp_details.category_two, role=cfp_details.role_two)

                    context = {
                        'cfp_details': cfp_details,
                        'user_data': user_details,
                        'user_contact': user_contact,
                        'user_education': user_education,
                        'lists': lists,
                        'lists2': lists2
                    }
                    return render(request, 'virtualmain_pages/user-profile.html', context)

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
        t_id = datas.id
        print(t_id)
        if request.method == "POST":
            if 'course_submit' in request.POST:
                title = request.POST["title"]
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

        context ={
            'datas' : datas,
            'req_list':req_list,
            'learn_list':learn_list,
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
                less_private = random.randint(112,1000)*100

                Less = Lesson(lesson_name=lesson_name,lesson_private=less_private,lesson_id_id=c_id)
                Less.save()
                messages.success(request,"Lesson Added")
                print("success")

            if 'addTopic' in request.POST:
                topic_caption = request.POST['topic_descrip']
                topic_video = request.POST['topic_video']
                lesson = request.POST['les_id']
                # Video duration

                # video = VideoFileClip(topic_video.temporary_file_path())
                # print("Duration")
                # video_sec = video.duration
                # video_hr = str(dt.timedelta(seconds=video_sec))
                # print(video_hr)
                # video_dur = video_hr[:video_hr.index('.')]

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
    cfp_list=CFP_role.objects.all()
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


            proj=ProjectManager.objects.create(
                project_title=project_title,
                project_description=project_description,
                project_thumbnail=project_thumbnail,
                project_duration=project_duration,
                candidates_required=candidates_required,
                project_docs=project_docs,
                project_category=project_category,
                project_cfp=project_cfp
            )
            # proj.project_cfp.set(cfp_list)
            proj.save()

            obj=ProjectCFPStore.objects.all().delete()
            return redirect("/projectmanager/")


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


def projectDashboard(request):
    projects=ProjectManager.objects.all()
    context={
        'projects':projects,
    }
    return render(request,'ProjectModule_Pages/Project_dashboard.html',context)


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
            return redirect('/cfp_create/')

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



def pricing(request):

    return render(request,"virtualmain_pages/pricing.html")
