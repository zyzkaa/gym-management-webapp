from time import strftime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from users.models import User, Visit, Membership
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
            form.save()
            form = ClientRegisterForm()
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
            if not user.is_coach:
                login(request, user)
            return HttpResponseRedirect('/users/profile')

    context['form'] = form
    return render(request, 'users/login.html', context)

def logout_user(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
    return redirect("/")

@login_required
def user_current_profile(request):
    user = request.user
    workouts = Workout.objects.filter(client=user)
    context = {
        'user': user,
        'workouts': workouts,
        }
    return render(request, 'users/profile.html', context)



def coach_profile(request):
    return render(request, 'users/coach_profile.html')

def user_profile(request):
    return render(request, 'users/user_profile.html')

from datetime import date, datetime
def add_visit(request, user_id):
    #user_id = request.user_id
    try:
        user = User.objects.get(pk=user_id)
        visit = Visit.objects.create(client=user, date=date.today(), enter_time=datetime.now().strftime("%H:%M:%S"))
        visit.save()
        return HttpResponse('ok')
    except User.DoesNotExist:
        return HttpResponse('no such user')

def show_memberships(request):
    memberships = Membership.objects.all()
    context = {
        'memberships': memberships,
    }
    return render(request, 'users/membership.html', context)


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