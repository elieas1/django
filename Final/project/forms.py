from django import forms
from django.core.exceptions import ValidationError
from .models import User, Post, Email


class registeruser(forms.Form):
    username = forms.CharField(
        label='', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class': 'login', 'placeholder': 'Username', 'autocomplete': 'off'}))
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'login', 'placeholder': 'Email','autocomplete':'off'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'login', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': 'login', 'placeholder': 'Password Confirmation'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if not username.isalnum():
            raise ValidationError(
                "Username can only contain letters and numbers")
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class postform(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={
                           "placeholder": "Enter Your Text Here", "rows": 15, "cols": 70, "id": "formbody"}))
    title = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Add Title', 'id': 'formtitle'}))

    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'category',
        ]


class emailform(forms.ModelForm):
    recipient = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'id': 'compose-recipients', 'class': 'form-control', 'placeholder': 'Recipient'}))
    body = forms.CharField(widget=forms.Textarea(attrs={
                           'id': 'compose-body', 'class': 'form-control', 'placeholder': 'Message', 'rows': 6}))

    class Meta:
        model = Email
        fields = [
            'recipient',
            'subject',
            'body'
        ]

        widgets = {
            'subject': forms.TextInput(attrs={'id': 'compose-subject', 'class': 'form-control', 'placeholder': 'Subject'}),
        }
