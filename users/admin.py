from dataclasses import fields
from operator import indexOf

from django.contrib import admin
from users.models import User, Coach
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Other',
            {
                'fields': ['is_coach', 'gender', 'profile_picture']
            }
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change and form.cleaned_data.get('password'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Coach)
