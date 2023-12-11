from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=250, required=True)
    password  =forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password",)
        def clean_username(self):
            username = self.cleaned_data.get('username')
            model = self.Meta.model
            username = model.objects.filter(username__iexact=username)           
            if user.exists():
                raise forms.ValidationError("A user with that name already exists")
            return self.cleaned_data.get('username')

    
        def clean_email(self):
            email = self.cleaned_data.get('email')
            model = self.Meta.model
            email = model.objects.filter(email__iexact=email)           
            if email.exists():
                raise forms.ValidationError(request,"A user with that email")
            return self.cleaned_data.get('email')

        def clean_password(self):
            password = self.cleaned_data.get('password')
            confirm_password = self.data.get('confirm_password')
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")
            return self.cleaned_data.get('password')
           


class UserProfileUpdateForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "new_password", "confirm_password")

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
        return self.cleaned_data.get('email')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match")
            
            self.instance.set_password(new_password)
            self.instance.save()

        return cleaned_data

       
class ProfilePictureUpdateForm(forms.Form):
    profile_image = forms.ImageField(required=True)          