from django import forms

from users.models import User, Client

class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        client = Client.objects.create(user=user)
        client.save()
        return client

class ClientLoginForm(forms.ModelForm):
    class Meta:
        fields = ['email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        client = Client.objects.create(user=user)
        client.save()
        return client