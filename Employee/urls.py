from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/',views.adduser,name='register'),
    path('',views.userlogin,name='login'),
    path('logout/', views.logout, name='logout'),
    path('userdashboard/',views.userdashboard,name='dashboard'),
    path('admindashboard',views.adminDashboard,name="admindashboard"),
    ]