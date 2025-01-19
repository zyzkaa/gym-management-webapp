from lib2to3.fixes.fix_input import context
from time import strftime
from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import request

from users.models import User, Visit, Coach
from memberships.models import Membership, Payment
from django.contrib.auth import login, logout

# dodaj wizyty, moze jakis qr kod?
# moze laczenie z zegarkami czy cos do treningow

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
            return redirect('/users/memberships')
        else:
            error = form.errors
            return HttpResponse('error' + str(error))

    context['form'] = form
    return render(request, 'users/register.html', context)

def login_user(request):
    context = {}
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')

    context['form'] = form
    return render(request, 'users/login.html', context)

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
        #workouts = Workout.objects.filter(coach=user)
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

def edit_info(request):
    user = request.user
    if user.is_coach:
        data = {
            'hourly_rate': user.coach.hourly_rate,
            'description': user.coach.description,
            'phone_number': user.coach.phone_number,
        }
        if request.method == 'POST':
            form = CoachEditForm(request.POST, instance=user, initial=data)
            form.save()
            for name, value in data.items():
                if form.cleaned_data[name] != value:
                    setattr(user.coach, name, form.cleaned_data[name])
            user.coach.save()
            return redirect('users:current_profile')
        form = CoachEditForm(instance=request.user, initial=data)
    else:
        if request.method == 'POST':
            form = UserEditFrom(request.POST, instance=request.user)
            form.save()
            return redirect('users:current_profile')
        form = UserEditFrom(instance=request.user)
    return render(request, 'users/login.html', {'form': form})

# def register(request):
#     if request.method == "POST":
#         form = ClientRegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = User(username=username, password=make_password(password))
#             user.save()
#             return HttpResponse("success")
#     else:
#         form = ClientRegisterForm()
#
#     return render(request, 'users/register.html', {form: form})


# # ...
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})