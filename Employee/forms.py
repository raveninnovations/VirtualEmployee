from django import forms
from django.forms import ModelForm

from .models import UserDetails,User
from django.contrib.auth import authenticate

from phonenumber_field.formfields import PhoneNumberField
class AddUserForm(ModelForm):
    class Meta:
        model = UserDetails
        fields=['user_phone']


# class EditUserProfileForm(ModelForm):
#
# 	class Meta:
# 		model = UserProfile
#
# 		fields = [
# 		'user_profile',
# 		'gender',
# 		'address',
# 		'degree',
# 		'specialisation',
# 		'current_year',
# 		'institution_name',
# 		'institution_address',
# 		'career_category',
# 		'career_specification'
#
# 		]

