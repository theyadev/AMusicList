from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm

from ..models import Song, Staff, Lists


def index(request):
    return HttpResponse("Hello, world. You're at the main index.")


def song(request, songId):
    try:
        song = Song.objects.get(id=songId)
    except Song.DoesNotExist:
        return render(request, "404.html")

    context = {"song": song, "in_list": False, "favourite": False}

    try:
        song_in_list = Lists.objects.get(user=request.user, song=song)

        context["in_list"] = True
        context["favourite"] = song_in_list.favourite
    except:
        pass

    return render(request, "song.html", context)


def artist(request, staffId):
    try:
        artist = Staff.objects.get(id=staffId)
    except Staff.DoesNotExist:
        return render(request, "404.html")

    return render(request, "artist.html", {"artist": artist})


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    context = {"form": LoginForm()}

    return render(request, "login.html", context)


def signup(request):
    context = {"form": SignupForm()}

    if request.user.is_authenticated:
        return redirect("/")

    return render(request, "signup.html", context)
