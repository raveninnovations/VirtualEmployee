"""VirtualMain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # path('', include('Admin.urls')),
    path('', include('Employee.urls')),
    path('admin_log/', admin.site.urls),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_sent.html'),
         name="password_reset_done"),

    path('reset_password_sent/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
         name="password_reset_complete"),

]
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'Employee.views.error_404_view'
handler500 = 'Employee.views.error_500_view'