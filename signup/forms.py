from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Doctor


def validate_id_num(value):
    for i in tuple(value):
        try:
            int(i)
        except:
            raise ValidationError(
                _("%(value)s is not a number"),
                params={"value": value},
        )



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(min_length=1, max_length=30, required=True)
    last_name = forms.CharField(min_length=1, max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    national_id = forms.CharField(max_length=10, min_length=10, required=True, validators=[validate_id_num])
    profile_picture = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2','id','profile_picture')

        



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)




class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput())
    national_id = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}))

    class Meta:
        model = Doctor
        fields = ['national_id', 'profile_picture']