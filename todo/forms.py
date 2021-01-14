import re
from django import forms
from . models import NewUserTodo
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class NewUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email"]

    def clean(self):
        all_data = super().clean()

        first_name, last_name = all_data.get(
            "first_name"), all_data.get("last_name")

        email = all_data.get("email")

        check_first = re.compile(r"^[a-zA-Z]+$").search(first_name)

        check_last = re.compile(r"^[a-zA-Z]+$").search(last_name)

        if not check_first:
            raise ValidationError(
                "Only instance of Letter should be in your firstname.")

        if not check_last:
            raise ValidationError(
                "Only instance of Letter should be in your lastname.")

        if not email.endswith("com"):
            raise ValidationError(
                "Email should end with .com")


class NewUserTodoForm(forms.ModelForm):
    class Meta:
        model = NewUserTodo
        fields = ("title", "memo", "important")
