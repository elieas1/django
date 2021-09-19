from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import User


class registeruser(forms.Form):
    firstname = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'registerInput', 'placeholder': 'First Name'}))
    lastname = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'registerInput', 'placeholder': 'Last Name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'registerInput', 'placeholder': 'Email', 'autocomplete': 'off'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'registerInput', 'placeholder': 'Password'}))
    password_conf = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': 'registerInput', 'placeholder': 'Password Confirmation'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                print('user is not active')
                return email
            else:
                raise ValidationError("Email already exists")
        except ValidationError:
            raise ValidationError("Email already exists")
        except ObjectDoesNotExist:
            return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise ValidationError("Password should be 8 characters or more")

        return password

    def save(self, commit=True):
        user = User.objects.create(
            email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        return user
