from django.urls import path


from . import views

urlpatterns = [
    path('register/',views.adduser,name='register'),
    path('login/',views.userlogin,name='login'),
    path('userdashboard/',views.userdashboard,name='dashboard'),

    ]