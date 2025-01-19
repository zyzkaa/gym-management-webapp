from warnings import catch_warnings
from xml.etree.ElementTree import tostring

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
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
            return HttpResponse(f'joined {workout_id}')
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
    workout_id = request.GET.get('workout_id')
    workout = Workout.objects.get(id=workout_id)
    if workout.coach != request.user:
        return HttpResponse('not authorized')
    if request.method == "POST":
        form = AddWorkoutForm(request.POST, instance=workout)
        form.save()
        return redirect("users:current_profile")
    form = AddWorkoutForm(instance=workout)
    return render(request, "workout/add.html", {'form': form})

def log_visit(request):
    return HttpResponse('ok')

