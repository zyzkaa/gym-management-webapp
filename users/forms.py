from dataclasses import field

from django import forms
from django.contrib.auth import validators
from django.contrib.auth.password_validation import validate_password

from users.models import User, Client, Payment
from utils import delete_null_choice


class ClientRegisterForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput(),
    #                            validators=[validate_password])
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=20,
                               validators=[validators.UnicodeUsernameValidator()],
                               error_messages={'unique': 'user with that username already exists'})
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender']
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'custom'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            client = Client.objects.create(user=user)
            return client


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = delete_null_choice(self.fields['gender'].choices)
        print(type(self.fields['gender'].choices))

# do wyjebania
# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = ['method']
#         widgets = {
#             'method': forms.RadioSelect(),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['method'].choices = delete_null_choice(self.fields['method'].choices)

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