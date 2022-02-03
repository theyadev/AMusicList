from django.shortcuts import redirect, render
from django.views.generic import DetailView, FormView
from django.urls import reverse
from .models import User, Lists, Activities
from django.contrib.auth import logout, login
from .forms import LoginForm, SignupForm

from django.views import View

from songs.models import Song, Artist

from random import choice


def getRedirect(request):
    """
    Return the "to" parameter from a request, return "/" if no parameter
    """
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

        return self.get(self.request)


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

        return redirect("/song/" + str(songId))


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
                return redirect("/song/" + str(songId))

        return redirect("/song/" + str(songId))


class UserView(DetailView):
    template_name = "users/user.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user
        context["is_following"] = (
            self.get_object().user_followers.filter(id=self.request.user.id).exists()
        )

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
