from django.shortcuts import render
from django.http import HttpResponse
from users.models import User
from django.contrib.auth.hashers import make_password

def get_username(request, user_id):
    return HttpResponse("ur looking at user of id: " + str(user_id))

from forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User(username=username, password=make_password(password))
            user.save()
            return HttpResponse("success")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {form: form})



def get_users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'users/index.html', context)


# # ...
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})