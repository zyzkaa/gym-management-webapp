from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from workout.forms import AddWorkoutForm

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
            return HttpResponseRedirect("/users/profile")
    context["form"] = form
    return render(request, "workout/add.html", context)

def schedule(request):
    context = {}
    return render(request, "workout/schedule.html", context)