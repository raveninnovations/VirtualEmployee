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
    # User Section
    path('userdashboard/',views.userdashboard,name='dashboard'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('user-profile-edit/',views.userEdit,name='userprofileEdit'),
    path('user-project/',views.userProject,name='userproject'),
    # CSM Section
    path('csmdashboard/',views.csmDashboard,name='csmDashboard'),
    path('csmaddcourse/',views.csmAddCourse,name='csmAddCourse'),
    # TL Section
    path('tldashboard/',views.tlDashboard,name='tlDashboard'),
    path('tl-projectdetails/',views.tlProjectDetails,name='tlProjectDetails'),
    # PROJECT Section
    path('projectmanager/',views.projectManager,name='projectManager'),
    path('projectdashboard/',views.projectDashboard,name='projectDashboard'),
    ]