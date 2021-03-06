from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import List
from .models import Profile
from .validators import validate_email


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
    #             'Please use another Email, that is already taken')
    #     return email


class UpdateDetailForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ["content"]

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["image"]
