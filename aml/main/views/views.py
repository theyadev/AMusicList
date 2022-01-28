from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.views import View

from ..forms import LoginForm, SignupForm

from ..models import Activities, Album, Song, Artist, Lists, User

from django.views.generic import DetailView, FormView


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
        if (
            self.request.user.is_authenticated
            and Lists.objects.filter(
                user=self.request.user, song=self.get_object()
            ).exists()
        ):
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


class MainView(View):
    template_name = "index.html"
    template_name_logged = "logged_index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_list = [request.user]
            user_list.extend(request.user.follows.all())

            activites = Activities.objects.filter(user__in=user_list)
            activites = sorted(
                activites, key=lambda activity: activity.date, reverse=True
            )

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

            return render(request, self.template_name_logged, context)

        return render(request, self.template_name)


def getRedirect(request):
    try:
        return request.GET["to"]
    except:
        return "/"


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        redirect_url = getRedirect(request)

        if request.user.is_authenticated:
            logout(request)

        return redirect(redirect_url)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        redirect_url = getRedirect(self.request)

        if request.user.is_authenticated:
            return redirect(redirect_url)

        context = {"form": self.form_class()}

        return render(request, self.template_name, context)

    def form_valid(self, form):
        redirect_url = getRedirect(self.request)

        user = form.get_user(self.request)

        if user is not None:
            login(self.request, user)
            return redirect(redirect_url)

        context = {"form": self.form_class()}

        return render(self.request, self.template_name, context)


class SignupView(LoginView):
    template_name = "signup.html"
    form_class = SignupForm
