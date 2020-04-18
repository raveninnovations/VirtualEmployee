from django.urls import path


from . import views

urlpatterns = [
    path('admin/',views.Login,name='login'),
    path('dashboard/',views.dasboard,name='dashboard'),
    ]