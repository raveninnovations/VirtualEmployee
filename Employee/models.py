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
    user_cfp = models.BooleanField(default=False,null=True)

    def __str__(self):
        return str(self.user_id) if self.user_id else ''


class UserContact(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    user_pic = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    user_bio=models.TextField(blank=False,null=True)


    def __str__(self):
        return self.address1

class UserEducation(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    start_month=models.CharField(max_length=100,blank=True)
    start_year=models.IntegerField(blank=True,default=0)
    end_month=models.CharField(max_length=100,blank=True)
    end_year=models.IntegerField( blank=True,default=0)
    institution = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100,blank=True)
    gpa=models.DecimalField( blank=False,default=0,max_digits=4, decimal_places=2)

    def __str__(self):
        return self.degree


class UserWorkExperience(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    start_month=models.CharField(max_length=100,blank=True)
    start_year=models.IntegerField(blank=True,default=0)
    end_month=models.CharField(max_length=100,blank=True)
    end_year=models.IntegerField( blank=True,default=0)
    job_role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.job_role


class UserSkill(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    category=models.CharField(max_length=100)
    skill=models.CharField(max_length=100)

    def __str__(self):
        return self.skill



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

class Week(models.Model):
    week_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    week_private = models.CharField(max_length=100,null=True)
    week_name = models.CharField(max_length=100)
    week_date = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return  self.week_name

class Week_Unit(models.Model):
    unit_id = models.ForeignKey(Week,on_delete=models.CASCADE)
    unit_caption = models.CharField(max_length=500)
    unit_video1 = models.FileField(upload_to="Week_Videos/",null=True)
    unit_video2 = models.FileField(upload_to="Week_Videos/",null=True)
    unit_video3 = models.FileField(upload_to="Week_Videos/",null=True)
    def __str__(self):
        return self.unit_caption


class CareerCategory(models.Model):
    category_id=models.IntegerField(default=0)
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.category


class MicroCategory(models.Model):
    category_id=models.IntegerField(default=0)
    category=models.CharField(max_length=255)

    def __str__(self):
        return self.category

class MicroCourse(models.Model):
    c_id = models.ForeignKey(MicroCategory,on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    video = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.course_name


class SubCategory(models.Model):
    cat_id=models.ForeignKey(CareerCategory,on_delete=models.CASCADE,null=True)
    sub_category=models.CharField(max_length=255,null=True)
    create_date=models.DateTimeField(default=datetime.now,null=True)

    def __str__(self):
        return self.sub_category
class CategoryCourse(models.Model):
    cat_id = models.ForeignKey(CareerCategory,on_delete=models.CASCADE)
    sub_id = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    cfp = models.CharField(max_length=200)

    def __str__(self):
        return self.cfp


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
    project_status=models.CharField(max_length=200, blank=True)
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
    user_id = models.ForeignKey(User,models.CASCADE,null=True)
    cat_id = models.ForeignKey(CareerCategory,models.CASCADE,null=True)
    sub_id = models.ForeignKey(SubCategory,models.CASCADE,null=True)
    cfp_id = models.ForeignKey(CategoryCourse,models.CASCADE,null=True)

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
    video = models.ForeignKey(Week_Unit,models.CASCADE,null=True)
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
    course_tag = models.CharField(max_length=100,null=True)
class CourseTag(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True)
    course_tag = models.CharField(max_length=100,null=True)
    course_role = models.CharField(max_length=100,null=True)
    points = models.CharField(max_length=50,null=True)

class ProjectPoint(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE,null=True)
    proj_points = models.CharField(max_length=50,null=True)
    proj_role = models.CharField(max_length=100,null=True)


#  Certificate

class Certificate(models.Model):
    user_id = models.ForeignKey(UserContact,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    certi_topic = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    serial_key = models.CharField(max_length=100,null=True)
    issue_date = models.CharField(max_length=50,null=True)
    certi_img = models.ImageField(upload_to='certificates/',null=True)
    certi_choose = models.CharField(max_length=20,null=True)
    # certi_img1 = models.ImageField(upload_to='certificates/',null=True)

    def __str__(self):
        return self.certi_topic

class Reference(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=200)
    used_peoples = models.IntegerField(default=0,null=True)
    used_id = models.CharField(max_length=10,null=True)

class EmiPlan(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    first_emi = models.IntegerField()


class BlogManager(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    blog_title=models.CharField(max_length=100)
    blog_tagline=models.CharField(max_length=150,blank=True)
    blog_body=models.TextField(blank=True)
    blog_thumbnail=models.ImageField(upload_to='blog_images/',null=True,blank=True)
    blog_category=models.CharField(max_length=200,null=True, blank=True)
    blog_date = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.blog_title


class BlogHeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blog_title = models.CharField(max_length=100)
    blog_body = models.TextField(blank=True)
    blog_thumbnail = models.ImageField(upload_to='blog_highlight/', null=True, blank=True)
    blog_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.blog_title


class BlogCategory(models.Model):
    blog_category_id=models.IntegerField(default=0)
    blog_category=models.CharField(max_length=255)

    def __str__(self):
        return self.blog_category


# Quizz
class Quizz(models.Model):
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    ques_no = models.IntegerField(null=True)
    question = models.CharField(max_length=250)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question




