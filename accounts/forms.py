from django import forms
from . models import CustomUser
from django.core.validators import FileExtensionValidator
import re


class CustomUserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'username_required': "User name is a required field.",
        'username_rules': "User name must not contain any special character aside from space.",
        'valid_images': "Image uploaded is not in valid form, must be in png or jpg format!",
        'password_length': "Your password is not secure enough, must be at least 8 characters long.",
        'password_security': "Your password must contain at least 1 number and a capital letter.",
        'file_size_exceeded': "File size exceeded, please upload an image whose size is less than 1 MB."
    }
    password1 = forms.CharField(label=("Please Enter Your Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=("Please Confirm Your Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=("Enter the same password as above, for verification."))
    username = forms.CharField(label=("Please Enter Username"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=("Please Enter Your Email"),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.FileField(label=("Please Upload Your Profile Image"),
                                    widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                                    validators=[FileExtensionValidator(['png', 'jpg'])])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_image',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(
                self.error_messages['username_required'],
                code='username_required'
            )

        pattern = '^[^0-9][a-zA-Z0-9_ ]+$'
        result = re.match(pattern, username)

        if username and not result:
            raise forms.ValidationError(
                self.error_messages['username_rules'],
                code='username_rules'
            )
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError(
                self.error_messages['password_length'],
                code='password_length'
            )
        pattern = '[A-Za-z0-9@#$%^&+=]+'
        result = re.fullmatch(pattern, password)

        if len(password) > 8 and not result:
            raise forms.ValidationError(
                self.error_messages['password_security'],
                code='password_security'
            )

        return password

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image.size > 1048576:
            raise forms.ValidationError(
                self.error_messages['file_size_exceeded'],
                code='file_size_exceeded'
            )
        return profile_image

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
