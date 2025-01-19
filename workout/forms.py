from django import forms
from datetime import time, timedelta
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

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        day = cleaned_data.get('day')

        workouts = Workout.objects.filter(day=day)
        for workout in workouts:
            if (workout.start_time < start_time < workout.end_time
                or workout.start_time < end_time < workout.end_time
            or start_time < time(6,0)
            or end_time > time(22, 0)
            or (end_time.hour - start_time.hour) > 1):
                raise forms.ValidationError("This time is not available")

        return cleaned_data