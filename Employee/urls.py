from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/',views.adduser,name='register'),
    path('',views.userlogin,name='login'),
    path('logout/', views.logout, name='logout'),
    path('admindashboard/',views.adminDashboard,name="admindashboard"),
    path('admindashboard/courses/',views.adminCourses,name='admincourse'),
    path('admindashboard/projects/',views.adminProjects,name='adminprojects'),
    path('admindashboard/role_creation/',views.adminRolecreation,name='adminrolecreation'),
    path('admindashboard/admin_license/',views.adminLicense,name='adminLicense'),
    path('admindashboard/license_info/<int:id>', views.adminLicenseInfo, name='licenseInfo'),
    path('admindashboard/cfp_create/',views.cfp_create,name='cfp_create'),
    path('admindashboard/cfp_edit/<int:id>',views.cfp_edit,name='cfpEdit'),
    # User Section
    path('userdashboard/',views.userdashboard,name='dashboard'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('user-profile-edit/',views.userEdit,name='userprofileEdit'),
    path('user-project/',views.userProject,name='userproject'),
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
    path('tl-projectdetails/',views.tlProjectDetails,name='tlProjectDetails'),
    # PROJECT Section
    path('projectmanager/',views.projectManager,name='projectManager'),
    path('projecteditmanager/<int:id>',views.projectEditManager,name='projectEditManager'),
    path('projectdashboard/',views.projectDashboard,name='projectDashboard'),
    #Create category and CFP

    path('category_edit/<int:id>',views.category_edit,name='categoryEdit'),
    path('createcourse/',views.createcourse,name='createcourse'),
    path('testEdit/<int:id>',views.testEdit,name='testEdit'),
    # path('careerchoice/',views.careerchoice,name='careerchoice'),
    path('usercfp/', views.UserCfp, name='usercfp'),
    path('pricing/',views.pricing,name='pricing')
    ]
