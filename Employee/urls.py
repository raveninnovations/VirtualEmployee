from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/',views.adduser,name='register'),
    path('',views.userlogin,name='login'),
    path('logout/', views.logout, name='logout'),
    path('admindashboard/',views.adminDashboard,name="admindashboard"),
    path('courses/',views.adminCourses,name='admincourse'),
    path('add_course/',views.adminAddcourse,name='adminaddcourse'),
    path('projects/',views.adminProjects,name='adminprojects'),
    path('role_creation/',views.adminRolecreation,name='adminrolecreation'),
    path('admin_license/',views.adminLicense,name='adminLicense'),
    # User Section
    path('userdashboard/',views.userdashboard,name='dashboard'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('user-profile-edit/',views.userEdit,name='userprofileEdit'),
    path('user-project/',views.userProject,name='userproject'),
    path('user-course/<int:id>', views.userCourse, name='usercourse'),
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
    path('tl-projectdetails/',views.tlProjectDetails,name='tlProjectDetails'),
    # PROJECT Section
    path('projectmanager/',views.projectManager,name='projectManager'),
    path('projectdashboard/',views.projectDashboard,name='projectDashboard'),
    #Create category and CFP
    path('cfp_create/',views.cfp_create,name='cfp_create'),
    path('cfp_edit/<int:id>',views.cfp_edit,name='cfpEdit'),
    path('category_edit/<int:id>',views.category_edit,name='categoryEdit'),
    path('test/',views.test,name='test'),
    # path('careerchoice/',views.careerchoice,name='careerchoice'),
    path('usercfp/', views.UserCfp, name='usercfp'),
    path('pricing/',views.pricing,name='pricing')
    ]
