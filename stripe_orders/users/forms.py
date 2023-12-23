from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Enter your username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control py-4", "placeholder": "Enter your password"})
    )


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control py-4",
                    "placeholder": "Enter username",
                }
            ),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control py-4", "placeholder": "Enter a password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control py-4", "placeholder": "Confirm password"}))
