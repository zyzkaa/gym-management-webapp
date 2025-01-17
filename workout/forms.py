from django import forms

from utils import delete_null_choice
from workout.models import Workout



class AddWorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        exclude = ('user', 'coach', 'status', 'client')
        widgets = {
            'difficulty': forms.RadioSelect(),
            'day' : forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['difficulty'].choices = delete_null_choice(self.fields['difficulty'].choices)
        self.fields['day'].choices = delete_null_choice(self.fields['day'].choices)