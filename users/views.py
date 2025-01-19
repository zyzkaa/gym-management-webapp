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

from users.forms import ClientRegisterForm
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

def logout_user(request):
    user = request.user
    if user.is_authenticated:
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