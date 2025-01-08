from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        })
    )

    password = forms.CharField(
        min_length=5,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
        })
    )