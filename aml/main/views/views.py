from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm

from ..models import Activities, Album, Song, Artist, Lists, User


def index(request):
    if request.user.is_authenticated:
        user_list = [request.user]
        user_list.extend(request.user.follows.all())

        activites = Activities.objects.filter(user__in=user_list)
        activites = sorted(activites, key=lambda activity: activity.date, reverse=True)

        activites_html = ""

        for activity in activites:
            user_html = (
                f'<a href="/user/{activity.user.id}">{activity.user.username}</a>'
            )
            song_html = (
                f'<a href="/song/{ activity.song.id }">{ activity.song.title }</a>'
            )

            if activity.action == "ADDED":
                text_html = f"{user_html} a ajouté {song_html} à sa liste !"
            elif activity.action == "REMOVED":
                text_html = f"{user_html} a retiré {song_html} de sa liste !"
            elif activity.action == "ADDED FAVOURITE":
                text_html = f"{user_html} a ajouté {song_html} à ses favoris !"
            elif activity.action == "REMOVED FAVOURITE":
                text_html = f"{user_html} a retiré {song_html} de ses favoris !"

            html = f"<p>{text_html}</p>"

            activites_html += html

        context = {"activities": activites_html}

        return render(request, "logged_index.html", context)

    return render(request, "index.html")


def user(request, userId):
    try:
        user = User.objects.get(id=userId)
    except User.DoesNotExist:
        return render(request, "404.html")

    if request.user.is_authenticated:
        is_following = len(request.user.follows.filter(id=user.id)) > 0
    else:
        is_following = False

    context = {
        "aml_user": user,
        "aml_user_list": Lists.objects.filter(user_id=userId),
        "following": is_following,
    }

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


def artist(request, artistId):
    try:
        artist = Artist.objects.get(id=artistId)
    except Artist.DoesNotExist:
        return render(request, "404.html")

    return render(request, "artist.html", {"artist": artist})


def album(request, albumId):
    try:
        album = Album.objects.get(id=albumId)
    except Album.DoesNotExist:
        return render(request, "404.html")

    return render(request, "album.html", {"album": album})

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
