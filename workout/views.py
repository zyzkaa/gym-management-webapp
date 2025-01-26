from lib2to3.fixes.fix_input import context
from warnings import catch_warnings
from xml.etree.ElementTree import tostring

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from users.models import User
from workout.forms import AddWorkoutForm
from workout.models import Workout


def is_coach(user):
    return user.is_coach

@login_required
@user_passes_test(is_coach, login_url='/')
def add_workout(request):
    context = {}
    form = AddWorkoutForm()
    if request.method == "POST":
        form = AddWorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.coach = request.user
            workout.save()
            return redirect("users:current_profile")
    context["form"] = form
    return render(request, "workout/add.html", context)

def schedule(request):
    context = {
        'workouts': Workout.objects.all(),
        # 'workouts': Workout.objects.all().order_by('start_time').values(),
        'weekdays': Workout.Weekdays.choices
    }
    return render(request, "workout/schedule.html", context)

@login_required
def join_workout(request):
    workout_id = request.GET.get('workout_id')
    try:
        workout = Workout.objects.get(id=workout_id)
        clients_count = workout.client.all().count()
        if workout.max_participants > clients_count: # test this!!
            workout.client.add(request.user)
            return redirect("workout:schedule")
        return HttpResponse(f'max participants already')
    except Workout.DoesNotExist:
        return HttpResponse('no such workout')

@login_required
def leave_workout(request):
    workout_id = request.GET.get('workout_id')
    try:
        workout = Workout.objects.get(id=workout_id)
        workout.client.remove(request.user)
        return HttpResponse(f'left {workout_id}')
    except Workout.DoesNotExist:
        return HttpResponse('no such workout')

@login_required
@user_passes_test(is_coach, login_url='/')
def delete_workout(request):
    workout_id = request.GET.get('workout_id')
    try:
        workout = Workout.objects.get(id=workout_id)
        if workout.coach == request.user:
            workout.client.clear()
            #print(workout.client.all())
            workout.status = 'inactive'
            workout.save()
        return redirect('users:current_profile')
    except Workout.DoesNotExist:
        return HttpResponse('no such workout')

def edit_workout(request):
    context = {
        'title': 'edit workout',
    }
    workout_id = request.GET.get('workout_id')
    workout = Workout.objects.get(id=workout_id)
    if workout.coach != request.user:
        return HttpResponse('not authorized')
    if request.method == "POST":
        form = AddWorkoutForm(request.POST, instance=workout)
        form.save()
        return redirect("users:current_profile")
    context['form'] = AddWorkoutForm(instance=workout)
    return render(request, "users/form.html", context)

def details_workout(request, workout_id):
    try:
        workout = Workout.objects.get(id=workout_id)
        context = {
            'workout': workout,
        }
        return render(request, "workout/details.html", context)
    except Workout.DoesNotExist:
        return HttpResponse('no such workout')

def remove_client_from_workout(request):
    workout_id = request.GET.get('workout_id')
    client_id = request.GET.get('client_id')
    workout = Workout.objects.get(id=workout_id)
    client = User.objects.get(id=client_id)
    workout.client.remove(client)
    workout.save()
    return redirect("workout:details_workout", workout_id)

