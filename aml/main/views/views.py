from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..forms import LoginForm, SignupForm

from ..models import Activities, Album, Song, Artist, Lists, User

from django.views.generic import DetailView


class UserView(DetailView):
    template_name = "user.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user
        context["is_following"] = (
            self.get_object().user_followers.filter(id=self.request.user.id).exists()
        )

        return context


class SongView(DetailView):
    template_name = "song.html"
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_entry"] = None
        if Lists.objects.filter(
            user=self.request.user, song=self.get_object()
        ).exists():
            context["list_entry"] = Lists.objects.get(
                user=self.request.user, song=self.get_object()
            )

        return context

class ArtistView(DetailView):
    template_name = "artist.html"

    model = Artist

class AlbumView(DetailView):
    template_name = "album.html"

    model = Album


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

# https://docs.djangoproject.com/en/4.0/ref/class-based-views/generic-editing/#formview

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
