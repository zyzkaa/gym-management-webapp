from django import forms

from workout.models import Workout


class AddWorkoutForm(forms.Form):
    class Meta:
        model = Workout
        exclude = ('user', 'coach', 'status')
        widgets = {
            'difficulty': forms.RadioSelect(),
            'day' : forms.RadioSelect(),
        }