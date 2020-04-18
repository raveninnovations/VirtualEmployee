from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('admin/',auth_views.LoginView.as_view(template_name='Admin_pages/form-modern-login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Admin_pages/logout.html'), name='logout'),
    path('dashboard/',views.dasboard,name='dashboard'),
    path('courses/', views.Courses, name='courses'),
    path('addCourse/', views.AddCourse, name='add-course'),
    ]