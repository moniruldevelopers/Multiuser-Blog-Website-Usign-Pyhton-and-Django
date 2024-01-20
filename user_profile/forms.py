from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password  =forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password",)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username)
        if user.exists():
            raise ValidationError("A user with that username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email)
        if user.exists():
            raise ValidationError("A user with that email already exists")

        # Check if the email domain is @gmail.com
        if not email.endswith('@gmail.com'):
            raise ValidationError("Only @gmail.com emails are allowed")

        return email


class UserProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username", "email", )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        
        if user.exists():
            raise forms.ValidationError("A user with that name already exists")
        
        return self.cleaned_data.get('username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        
        if user.exists():
            raise forms.ValidationError("A user with that email already exists")

        # Check if the email domain is @gmail.com
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Only @gmail.com emails are allowed")

        return email

    def change_password(self):
        if 'new_password' in self.data and 'confirm_password' in self.data:
            new_password = self.data['new_password']
            confirm_password = self.data['confirm_password']
            if new_password != '' and confirm_password != '':
                if new_password != confirm_password:
                    raise forms.ValidationError("Passwords do not match")
                else:
                    self.instance.set_password(new_password)
                    self.instance.save()

    def clean(self):
        self.change_password()   
class ProfilePictureUpdateForm(forms.Form):
    profile_image = forms.ImageField(required=True)          


