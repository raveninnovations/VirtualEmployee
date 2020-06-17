from django.contrib import admin

from .models import UserDetails,RoleDetail,Course,Lesson,Lesson_Topic,CareerCategory,CFP_role, ProjectManager,UserContact,UserEducation,CreateCourse,CareerChoice,StudentCFP,ProjectCFPStore,ProgressCourse,EnrolledProject,watched,Claim,CourseTag,ProjectPoint,UserWorkExperience

# Register your models here.

admin.site.register(UserDetails)
admin.site.register(RoleDetail)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Lesson_Topic)
admin.site.register(CareerCategory)
admin.site.register(CFP_role)
admin.site.register(ProjectManager)
admin.site.register(UserContact)
admin.site.register(UserEducation)
admin.site.register(UserWorkExperience)
admin.site.register(CreateCourse)
admin.site.register(CareerChoice)
admin.site.register(StudentCFP)
admin.site.register(ProjectCFPStore)
admin.site.register(ProgressCourse)
admin.site.register(EnrolledProject)
admin.site.register(watched)
admin.site.register(Claim)
admin.site.register(CourseTag)
admin.site.register(ProjectPoint)
