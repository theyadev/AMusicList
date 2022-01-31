from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.db.models import Q
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView

from ..forms import LoginForm, SignupForm
from ..models import Activities, Album, Song, Artist, Lists, User


def getRedirect(request):
    """
    Return the "to" parameter from a request, return "/" if no parameter
    """
    try:
        return request.GET["to"]
    except:
        return "/"


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favourite"] = (
            kwargs["object"].user_favourites.filter(pk=self.request.user.pk).exists()
        )

        return context

    def post(self, request, pk):
        if request.user.is_authenticated:
            try:
                artist = Artist.objects.get(pk=pk)

                if request.user.favourite_artists.filter(pk=pk).exists():
                    request.user.favourite_artists.remove(artist)
                else:
                    request.user.favourite_artists.add(artist)
            except:
                pass

        return redirect(reverse("artist", args=[pk]))


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


class SongsView(ListView):
    model = Song
    template_name = "songs.html"
    paginate_by = 100

    def get_queryset(self):
        filter_val = self.request.GET.get("search", "")
        order_val = self.request.GET.get("order", "title")

        queryset = (
            self.model.objects.filter(
                Q(title__icontains=filter_val) | Q(artists__name__icontains=filter_val)
            )
            .order_by(order_val)
            .distinct(order_val)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        context["order"] = self.request.GET.get("order", "title")

        get_copy = self.request.GET.copy()

        if get_copy.get("page"):
            get_copy.pop("page")

        context["get_copy"] = get_copy

        return context


class ArtistsView(SongsView):
    model = Artist
    template_name = "artists.html"

    def get_queryset(self):
        filter_val = self.request.GET.get("search", "")
        order_val = self.request.GET.get("order", "name")

        queryset = (
            self.model.objects.filter(name__icontains=filter_val)
            .order_by(order_val)
            .distinct(order_val)
        )

        return queryset


class AlbumsView(ArtistsView):
    model = Album
    template_name = "albums.html"

    def get_queryset(self):
        filter_val = self.request.GET.get("search", "")
        order_val = self.request.GET.get("order", "name")

        queryset = (
            self.model.objects.filter(
                Q(name__icontains=filter_val) | Q(artists__name__icontains=filter_val)
            )
            .order_by(order_val)
            .distinct(order_val)
        )

        return queryset
