from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .util import Player

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect(reverse('tables', kwargs={'name': username}))
        else:
            return render(request, "registration/login.html")
            #TODO

    return render(request, "registration/login.html")


def logout_page(request):
    print(request.user)
    logout(request)
    
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
    #TODO


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def tables(request, name):
    return render(request, "game/tables.html", {
        "name": name
    })


def table(request):
    if request.method == "POST":
        player = Player()
        player.set_is_sitting(True)

        return render(request, "game/table.html")
    print(request.session)

    return render(request, "game/table.html")


def error(request):
    return HttpResponse("Error")
