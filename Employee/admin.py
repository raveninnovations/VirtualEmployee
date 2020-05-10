from django.contrib import admin
from .models import UserDetails,RoleDetail,Course
# Register your models here.

admin.site.register(UserDetails)
admin.site.register(RoleDetail)
admin.site.register(Course)
