from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm

from ..models import Activities, Song, Staff, Lists, User


def index(request):
    if request.user.is_authenticated:
        activites = Activities.objects.filter(user=request.user)
        activites = sorted(activites, key=lambda activity: activity.date, reverse=True)
        context = {"activities": activites}
        return render(request, "logged_index.html", context)

    return render(request, "index.html")


def user(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return render(request, "404.html")

    context = {"aml_user": user, "aml_user_list": Lists.objects.filter(user_id=userId)}

    return render(request, "user.html", context)


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
    try:
        redirect_url = request.GET["to"]
    except:
        redirect_url = "/"

    if request.user.is_authenticated:
        return redirect(redirect_url)

    context = {"form": LoginForm()}

    return render(request, "login.html", context)


def signup(request):
    context = {"form": SignupForm()}

    if request.user.is_authenticated:
        return redirect("/")

    return render(request, "signup.html", context)
