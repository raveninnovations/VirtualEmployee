from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

CATEGORY_CHOICES = (
    ('IT', 'IT & Software'),
    ('Business & Startups', 'Business & Startups'),
    ('Designing', 'Designing'),
    ('Electronics & Electricals', 'Electronics & Electricals'),
)
DIFFICULTY_LEVEL=(
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
)

class AdminLicense(models.Model):
    key = models.CharField(max_length=100)
    years =  models.IntegerField()
    date = models.DateTimeField(default=datetime.now,null=True)
    def __str__(self):
        return self.key

class UsedLicense(models.Model):
    u_key = models.CharField(max_length=100)
    u_years =  models.IntegerField()
    u_date = models.DateTimeField(default=datetime.now,null=True)

    def __str__(self):
        return self.u_key

class UserDetails(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    user_phone = PhoneNumberField(null=False, blank=False, unique=False, default='+91')
    user_pass = models.CharField(max_length=10, blank=True)
    user_unique = models.CharField(max_length=100,null=True)
    user_date = models.DateTimeField(default=datetime.now,null=True)
    user_license = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.user_id) if self.user_id else ''


class UserContact(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    user_pic = models.ImageField(upload_to='user_profile/', null=True, blank=True)


    def __str__(self):
        return self.address1

class UserEducation(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    year = models.IntegerField()
    institution = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.degree



class RoleDetail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    role_user_id=models.CharField(max_length=10)
    user_role=models.CharField(max_length=255)
    role_user_name=models.CharField(max_length=255)
    role_user_email=models.CharField(max_length=255)
    role_user_password=models.CharField(max_length=255)
    role_create_date=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.role_user_name

# class UserProfile(models.Model):
#
# 	user_id = models.ForeignKey(User,on_delete=models.CASCADE)
# 	user_profile 		 = models.ImageField(upload_to='user_profile/')
# 	gender               = models.CharField(max_length=50)
# 	address              = models.CharField(max_length=200)
# 	degree               = models.CharField(max_length=50)
# 	specialisation       = models.CharField(max_length=50)
# 	current_year 	     = models.CharField(max_length=50)
# 	institution_name     = models.CharField(max_length=100)
# 	institution_address  = models.CharField(max_length=200)
# 	career_category      = models.CharField(max_length=50)
# 	career_specification = models.CharField(max_length=50)
#
# 	def __str__(self):
# 		return str(self.first_name+" "+self.last_name)

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=datetime.now, null=True)
    title = models.CharField(max_length=50)
    tagline=models.CharField(max_length=50)
    short_description=models.CharField(max_length=100)
    course_image=models.ImageField(upload_to='csm_images/',null=True,blank=True)
    category=models.CharField(max_length=30, choices=CATEGORY_CHOICES,null=True,blank=True)
    role=models.CharField(max_length=50,blank=True)
    course=models.CharField(max_length=50,blank=True)
    difficulty_level=models.CharField(max_length=20, choices=DIFFICULTY_LEVEL,null=True, blank=True)
    instructor=models.CharField(max_length=200,null=True, blank=True)

    # must add quiz Details

    # meta section
    meta_keywords=models.TextField(blank=True)
    meta_description=models.TextField(blank=True)

    # rewards
    course_points=models.IntegerField(default=0)
    certificate= models.CharField(max_length=200, null=True, blank=True)

    # Prerequisite
    requirements=models.TextField(blank=True)
    learnings=models.TextField(blank=True)


    def __str__(self):
        return self.title

class Lesson(models.Model):
    lesson_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson_private = models.CharField(max_length=100,null=True)
    lesson_name = models.CharField(max_length=100)
    lesson_date = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return  self.lesson_name

class Lesson_Topic(models.Model):
    topic_id = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    topic_caption = models.CharField(max_length=500)
    topic_video = models.CharField(max_length=500, null=True,blank=True)

    def __str__(self):
        return self.topic_caption


class CareerCategory(models.Model):
    category_id=models.IntegerField(default=0)
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.category


class CFP_role(models.Model):
    cfp_id=models.IntegerField(default=0)
    cfp_category=models.CharField(max_length=255)
    cfp_role=models.CharField(max_length=255)
    cfp_course=models.TextField(blank=True)
    cfp_create_date=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.cfp_role

class ProjectManager(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    project_title=models.CharField(max_length=100)
    project_description=models.TextField(blank=True)
    project_thumbnail=models.ImageField(upload_to='proj_images/',null=True,blank=True)
    project_duration=models.IntegerField()
    candidates_required=models.IntegerField(null=True)
    project_docs=models.FileField(upload_to='proj_docs/', null=True,blank=True)
    project_category=models.CharField(max_length=200,null=True, blank=True)
    project_cfp=models.CharField(max_length=200,null=True, blank=True)
    project_tl=models.CharField(max_length=200, blank=True)
    # project_cfp=models.ManyToManyField(CFP_role, related_name="cfp")
    def __str__(self):
        return self.project_title


class CreateCourse(models.Model):
    create_id=models.IntegerField(default=0)
    create_category=models.CharField(max_length=255)
    create_instructor=models.CharField(max_length=255,null=True)
    create_role=models.CharField(max_length=255,null=True)
    create_course=models.CharField(max_length=255)
    create_time=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.create_category



class CareerChoice(models.Model):
    career_id=models.IntegerField(default=0)
    choice_name=models.CharField(max_length=50,default="Student Choices")
    first_choice_category=models.CharField(max_length=50,blank=True)
    first_choice_role=models.CharField(max_length=50,blank=True,null=True)

    second_choice_category=models.CharField(max_length=50,blank=True)
    second_choice_role=models.CharField(max_length=50,blank=True,null=True)


    def __str__(self):
        return self.choice_name


class StudentCFP(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True)
    category_one = models.CharField(max_length=50,blank=True)
    role_one=models.CharField(max_length=50,blank=True)

    category_two=models.CharField(max_length=50,blank=True)
    role_two=models.CharField(max_length=50,blank=True)

    def _str__(self):
        return self.user_id


class ProjectCFPStore(models.Model):
    create_id=models.IntegerField(default=0)
    create_category=models.CharField(max_length=255)
    create_role=models.CharField(max_length=255,null=True)
    create_time=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.create_category


class ProgressCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course_id=models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    category=models.CharField(max_length=30,null=True,blank=True)
    role=models.CharField(max_length=50,blank=True)
    course=models.CharField(max_length=50,blank=True)
    course_image=models.ImageField(upload_to='progress_image/',null=True,blank=True)
    topics_count = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class EnrolledProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(ProjectManager, on_delete=models.CASCADE, null=True)
    enrolled_date=models.DateTimeField(default=datetime.now,blank=True)

# Watched videos
class watched(models.Model):
    video = models.ForeignKey(Lesson_Topic,models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=50)
    claim_reward = models.IntegerField(default=0,null=True)

# claim rewards
class Claim(models.Model):
    claim_id = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(UserDetails,models.CASCADE,null=True)
    points = models.CharField(max_length=50,null=True)
    category = models.CharField(max_length=100)
class CourseTag(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True)
    course_tag = models.CharField(max_length=100,null=True)
    course_role = models.CharField(max_length=100,null=True)
    points = models.CharField(max_length=50,null=True)

class ProjectPoint(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True)
    proj_points = models.CharField(max_length=50,null=True)
