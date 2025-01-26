import os.path
from dataclasses import field

from PIL import Image
from django import forms
from django.conf import settings
from django.contrib.auth import validators
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm, TextInput

from users.models import User, Client
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
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_coach = False
        if commit:
            user.save()
            client = Client.objects.create(user=user)
            return client


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = delete_null_choice(self.fields['gender'].choices)


class UserEditFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        picture = self.cleaned_data['profile_picture']
        if picture:
            picture_new = Image.open(picture)
            width, height = picture_new.size
            min_param = min(width, height)
            left = (width - min_param) / 2
            right = width - left
            top = (height - min_param) / 2
            bottom = height - top
            picture_new = picture_new.crop((left, top, right, bottom))
            new_path = 'profile_pictures/user_' + str(user.id) + '.webp'
            picture_new.save(os.path.join(settings.MEDIA_ROOT, new_path), format='WEBP')
            user.profile_picture = new_path
        if commit:
            user.save()
        return user


class CoachEditForm(UserEditFrom):
    hourly_rate = forms.DecimalField(max_digits=5, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(widget=forms.TextInput)

