from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Table
import json

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tables')
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


def tables(request):
    if request.user.is_authenticated:
        username = request.user.username

        tables = Table.objects.all()

        return render(request, "game/tables.html", {
            "name": username,
            "tables": tables
        })
    return redirect('login')


def table(request, table_name):
    return render(request, "game/table.html", {
        "table_name": table_name
    })


def error(request):
    return HttpResponse("Error")
