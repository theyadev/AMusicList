from django.shortcuts import redirect, render
from django.views.generic import DetailView, FormView
from django.urls import reverse
from .models import User, Lists, Activities
from django.templatetags.static import static
from django.contrib.auth import logout, login
from .forms import LoginForm, SignupForm

from django.views import View

from songs.models import Song, Artist

from random import choice


def getRedirect(request):
    """
    Return the "to" parameter from a request, return "/" if no parameter
    """

    value_to = request.GET.get("to", "/")
    value_to = "/" if value_to == "" else value_to

    return value_to


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        redirect_url = getRedirect(request)

        if request.user.is_authenticated:
            logout(request)

        return redirect(redirect_url)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        artists = Artist.objects.exclude(imageUrl="")

        context = {"form": self.form_class(), "artist": choice(artists.all())}

        return context

    def get(self, request, *args, **kwargs):
        redirect_url = getRedirect(self.request)

        if request.user.is_authenticated:
            return redirect(redirect_url)

        return render(request, self.template_name, self.get_context_data())

    def form_valid(self, form):
        user = form.get_user(self.request)

        if user is not None:
            login(self.request, user)

            redirect_url = getRedirect(self.request)
            return redirect(redirect_url)

        return redirect(self.request.get_full_path())


class SignupView(LoginView):
    template_name = "users/signup.html"
    form_class = SignupForm


class AddToListView(View):
    def post(self, request, songId):
        if request.user.is_authenticated:
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

        return redirect(reverse("song", args=[songId]))


class AddToFavourite(View):
    def post(self, request, songId):
        if request.user.is_authenticated:
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
                return redirect(reverse("song", args=[songId]))

        return redirect(reverse("song", args=[songId]))


class HomeView(View):
    template_name = "users/home.html"

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
                song_html = (
                    f'<a href="/song/{ activity.song.id }">{ activity.song.title }</a>'
                )

                if activity.action == "ADDED":
                    text_html = f"a ajouté {song_html} à sa liste !"
                elif activity.action == "REMOVED":
                    text_html = f"a retiré {song_html} de sa liste !"
                elif activity.action == "ADDED FAVOURITE":
                    text_html = f"a ajouté {song_html} à ses favoris !"
                elif activity.action == "REMOVED FAVOURITE":
                    text_html = f"a retiré {song_html} de ses favoris !"

                html = f"""
                <div class="card">
                    <img src="{activity.song.imageUrl}" alt="">
                    <div class="card-content">
                        <a href="/user/{activity.user.id}">{activity.user.username}</a>
                        <p class="card-text">{text_html}</p>
                        <img class="card-avatar" src="{static('users/avatar.png')}" alt="{activity.user.username}">
                    </div> 
                </div>"""

                activites_html += html

            context = {
                "activities": activites_html,
                "list": request.user.list.all()[:4],
                "active": "home"
            }

            return render(request, self.template_name, context)

        return redirect("login")


class UserView(DetailView):
    template_name = "users/user.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user
        context["is_following"] = (
            self.get_object().user_followers.filter(id=self.request.user.id).exists()
        )

        if context['object'].id == self.request.user.id:
            context['active'] = "user"

        return context

    def post(self, request, pk):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=pk)

                if request.user.follows.filter(pk=pk).exists():
                    request.user.follows.remove(user)
                else:
                    request.user.follows.add(user)
            except:
                pass

        return redirect(reverse("user", args=[pk]))
