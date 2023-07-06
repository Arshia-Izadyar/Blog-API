from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

custom_user = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label="Username", min_length=4, max_length=150)
    email = forms.EmailField(label="E mail")
    last_name = forms.CharField(label="Last name", max_length=150)
    first_name = forms.CharField(label="First name", max_length=150)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirm", widget=forms.PasswordInput)

    class Meta:
        model = custom_user
        fields = ("username", "last_name", "first_name")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = custom_user
        fields = UserChangeForm.Meta.fields
