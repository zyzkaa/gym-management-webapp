from django import forms
from django.contrib.auth import validators
from django.contrib.auth.password_validation import validate_password

from users.models import User, Client

class ClientRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[validate_password])
    username = forms.CharField(max_length=20,
                               validators=[validators.UnicodeUsernameValidator()],
                               error_messages={'unique': 'user with that username already exists'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']
        widgets = {
            'gender': forms.RadioSelect(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            client = Client.objects.create(user=user, gender=self.cleaned_data['gender'])
            return client

# class ClientLoginForm(forms.ModelForm):
#     class Meta:
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
#
#     def save(self, commit=True):
#         user = super().save(commit)
#         user.set_password(self.cleaned_data['password'])
#         client = Client.objects.create(user=user)
#         client.save()
#         return client