from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('',views.landing,name='landing'),
    path('register/',views.adduser,name='register'),
    path('Login/',views.userlogin,name='login'),
    path('activatecode/',views.activatecode,name='activatecode'),
    path('logout/', views.user_logout, name='logout'),
    path('admindashboard/',views.adminDashboard,name="admindashboard"),
    path('admindashboard/courses/',views.adminCourses,name='admincourse'),
    path('admindashboard/projects/',views.adminProjects,name='adminprojects'),
    path('admindashboard/role_creation/',views.adminRolecreation,name='adminrolecreation'),
    path('admindashboard/admin_license/',views.adminLicense,name='adminLicense'),
    path('admindashboard/license_info/<int:id>', views.adminLicenseInfo, name='licenseInfo'),
    path('admindashboard/cfp_create/',views.cfp_create,name='cfp_create'),
    path('admindashboard/cfp_edit/<int:id>',views.cfp_edit,name='cfpEdit'),
    path('admindashboard/student_info/', views.adminStudents, name='adminStudents'),
    # path('delete_student/<int:student_id>/', views.delete_student,name='delete_student'),
    # User Section
    path('userdashboard/',views.userdashboard,name='dashboard'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('user-profile-edit/',views.userEdit,name='userprofileEdit'),
    path('user-project/',views.userProject,name='userproject'),
    path('user-project-details/<int:id>',views.userProjectDetails,name='userprojectdetails'),
    path('user-course/<int:id>', views.userCourse, name='usercourse'),
    path('user-lesson/<int:id>', views.userLesson, name='userlesson'),
    path('user-change-password/',views.userchangepassword, name='userchangepassword'),
    # CSM Section
    path('csmdashboard/',views.csmDashboard,name='csmDashboard'),
    path('csmaddcourse/',views.csmAddCourse,name='csmAddCourse'),
    path('csmeditcourse/<int:id>',views.csmEditCourse,name='csmEditCourse'),
    path('csm-addcurriculam/<int:id>',views.csmAddCurriculam,name='csmAddCurriculam'),
    path('csm-editlesson/<int:id>', views.csmEditLesson,name='csmEditLesson'),
    path('csmsettings/',views.csmSettings,name='csmSettings'),
    # TL Section
    path('tldashboard/',views.tlDashboard,name='tlDashboard'),
    path('tl-projectdetails/<int:id>',views.tlProjectDetails,name='tlProjectDetails'),
    path('tl-projectstudentdetails/<int:pid>/<int:id>',views.tlProjectStudentDetails,name='tlProjectStudentDetails'),
    path('tl-settings/',views.tlSettings,name='tlSettings'),

    #Instructor Section
    path('instructordashboard/',views.insDashboard,name='insDashboard'),
    path('instructor_course_info/<int:id>',views.insCourseInfo,name='insCourseInfo'),

    # PROJECT Section
    path('projectmanager/',views.projectManager,name='projectManager'),
    path('projecteditmanager/<int:id>',views.projectEditManager,name='projectEditManager'),
    path('projectdashboard/',views.projectDashboard,name='projectDashboard'),
    path('pcmsettings/',views.pcmSettings,name='pcmSettings'),
    #Create category and CFP

    path('category_edit/<int:id>',views.category_edit,name='categoryEdit'),
    path('createcourse/',views.createcourse,name='createcourse'),
    path('testEdit/<int:id>',views.testEdit,name='testEdit'),
    # path('careerchoice/',views.careerchoice,name='careerchoice'),
    path('usercfp/', views.UserCfp, name='usercfp'),
    path('pricing/',views.pricing,name='pricing'),

    path('payment/',views.payment,name='payment'),

    #blog
    path('blogmanager/',views.blogManager,name='blogManager'),
    path('blogeditmanager/<int:id>',views.projectEditManager,name='blogEditManager'),
    path('blogdashboard/',views.blogDashboard,name='blogDashboard'),

    ]
