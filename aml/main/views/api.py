from django.forms import Form
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.views import View

from ..forms import LoginForm, SignupForm

from ..models import Song, User, Lists, Activities


def add_to_list(request, songId):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            song = Song.objects.get(id=songId)
        except Song.DoesNotExist:
            return render(request, "404.html")

        try:
            list_entry = Lists.objects.get(user=request.user, song=song)
            list_entry.delete()
            action = "REMOVED"
        except:
            list_entry = Lists(user=request.user, song=song, favourite=False)
            list_entry.save()
            action = "ADDED"

        activity = Activities(song=song, user=request.user, action=action)
        activity.save()

    return redirect("/song/" + str(songId))


def add_to_favourite(request, songId):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            song = Song.objects.get(id=songId)
        except Song.DoesNotExist:
            return render(request, "404.html")

        try:
            list_entry = Lists.objects.get(user=request.user, song=song)
            list_entry.favourite = not list_entry.favourite

            if list_entry.favourite:
                action = "ADDED FAVOURITE"
            else:
                action = "REMOVED FAVOURITE"

            list_entry.save()

            activity = Activities(song=song, user=request.user, action=action)
            activity.save()
        except:
            return redirect("/song/" + str(songId))

    return redirect("/song/" + str(songId))


def add_friend(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            redirect_url = request.GET["to"]
        except:
            redirect_url = "/"

        form = Form(request.POST)

        try:
            id = form.data["id"]
            user = User.objects.get(id=id)

            if request.user.follows.filter(id=user.id).exists():
                request.user.follows.remove(user)
            else:
                request.user.follows.add(user)
        except:
            return redirect("/404")

        return redirect(redirect_url)
