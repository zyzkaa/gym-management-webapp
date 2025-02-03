from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from users.models import User, Visit
from django.contrib.auth import login, logout
from users.forms import ClientRegisterForm, UserEditFrom, CoachEditForm
from workout.models import Workout


def register(request):
    context = {
        'title' : 'Register'
    }
    form = ClientRegisterForm()
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('memberships:show_memberships')
    context['form'] = form
    return render(request, 'users/form.html', context)

def login_user(request):
    context = {
        'title': 'Login'
    }
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')

    context['form'] = form
    return render(request, 'users/form.html', context)

@login_required
def logout_user(request):
    user = request.user
    logout(request)
    return redirect("/")

@login_required
def current_profile(request):
    user = request.user
    context = {
        'user': user
    }
    if user.is_coach:
        workouts = Workout.objects.filter(coach=user).filter(status='active')
        context['workouts'] = workouts
        return render(request, 'users/coach_profile.html', context)
    else:
        workouts = Workout.objects.filter(client=user)
        context['workouts'] = workouts
        return render(request, 'users/user_profile.html', context)

from datetime import date, datetime
def add_visit(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        visit = Visit.objects.create(client=user, date=date.today(), enter_time=datetime.now().strftime("%H:%M:%S"))
        visit.save()
        return HttpResponse('ok')
    except User.DoesNotExist:
        return HttpResponse('no such user')

def show_coaches(request):
    coaches = User.objects.filter(is_coach=True)
    context = {
        'coaches': coaches,
    }
    return render(request, 'users/coaches.html', context)

def coach_info(request, coach_id):
    try:
        coach = User.objects.get(id=coach_id)
        workouts = Workout.objects.filter(coach=coach)
        context = {
            'coach': coach,
            "workouts": workouts,
        }
        return render(request, 'users/coach_page.html', context)
    except User.DoesNotExist:
        return HttpResponse('no such user')

@login_required
def edit_info(request):
    user = request.user
    context = {
        'title': 'Edit profile'
    }
    if user.is_coach:
        data = {
            'hourly_rate': user.coach.hourly_rate,
            'description': user.coach.description,
            'phone_number': user.coach.phone_number,
        }
        context['form'] = CoachEditForm(instance=request.user, initial=data)
        if request.method == 'POST':
            form = CoachEditForm(request.POST, request.FILES, instance=user, initial=data)
            form.save()
            for name, value in data.items():
                if form.cleaned_data[name] != value:
                    setattr(user.coach, name, form.cleaned_data[name])
            user.coach.save()
            return redirect('users:current_profile')
    else:
        context['form'] = UserEditFrom(instance=request.user)
        if request.method == 'POST':
            form = UserEditFrom(request.POST, request.FILES, instance=request.user)
            form.save()
            return redirect('users:current_profile')
    return render(request, 'users/form.html', context)