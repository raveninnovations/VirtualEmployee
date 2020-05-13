from django.contrib import admin
from .models import UserDetails,RoleDetail,Course,Lesson,Lesson_Topic
# Register your models here.

admin.site.register(UserDetails)
admin.site.register(RoleDetail)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Lesson_Topic)

