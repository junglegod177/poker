from django.http import HttpResponse
from django.shortcuts import render, redirect

from .util import Player

# Create your views here.
def table(request):
    if request.method == "POST":
        player = Player()
        player.set_is_sitting(True)

        return render(request, "game/table.html")
    print(request.session)

    return render(request, "game/table.html")

def error(request):
    return HttpResponse("Error")
