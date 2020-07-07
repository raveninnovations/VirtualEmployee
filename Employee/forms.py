from django import forms
from django.forms import ModelForm

from .models import UserDetails,User
from django.contrib.auth import authenticate

from phonenumber_field.formfields import PhoneNumberField
class AddUserForm(ModelForm):
    class Meta:
        model = UserDetails
        fields=['user_phone']

