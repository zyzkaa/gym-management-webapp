from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag()
def get_workout_button(user, workout):
    result = {
        'name': 'edit',
        'class': 'details-button',
        'url': '',
    }
    if user == workout.coach:
        result['class'] += (' button-normal')
        result['url'] = reverse('workout:edit_workout') + f"?workout_id={workout.id}"
        return result
    elif user in workout.client.all():
        result['name'] = 'leave'
        result['class'] += (' button-normal')
        result['url'] = reverse('workout:leave_workout') + f"?workout_id={workout.id}"
        return result
    elif (workout.client.count() == workout.max_participants
          or user.client.membership is None
          or (user.client.membership.name != 'premium' and user.client_workouts.count() == 1)):
        result['class'] += (' button-locked')
        result['name'] = 'join'
        return result
    elif not user.is_coach:
        result['name'] = 'join'
        result['class'] += (' button-normal')
        result['url'] = reverse('workout:join_workout') + f"?workout_id={workout.id}"
        return result


