from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Item claim notifications will be sent here.'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
