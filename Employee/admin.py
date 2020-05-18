from django.contrib import admin
<<<<<<< HEAD
from .models import UserDetails,RoleDetail,Course,Lesson,Lesson_Topic,CareerCategory,CFP_role, ProjectManager
=======
from .models import UserDetails,RoleDetail,Course,Lesson,Lesson_Topic,CareerCategory,CFP_role,UserContact,UserEducation
>>>>>>> ca4bafa66c52953a1ae3ba523dc1c7a200b531dc
# Register your models here.

admin.site.register(UserDetails)
admin.site.register(RoleDetail)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Lesson_Topic)
admin.site.register(CareerCategory)
admin.site.register(CFP_role)
<<<<<<< HEAD
admin.site.register(ProjectManager)
=======
admin.site.register(UserContact)
admin.site.register(UserEducation)
>>>>>>> ca4bafa66c52953a1ae3ba523dc1c7a200b531dc
