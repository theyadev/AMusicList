from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.db.models import Q
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, FormView, ListView

from .models import Album, Song, Artist

from users.models import Activities, Lists


class SongView(DetailView):
    template_name = "song.html"
    model = Song

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_entry"] = None
        if self.request.user.is_authenticated:
            try:
                context["list_entry"] = Lists.objects.get(
                    user=self.request.user, song=self.get_object()
                )
            except Lists.DoesNotExist:
                pass

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
        """
        Add an artist to the favourite of a user
        """
        if request.user.is_authenticated:
            try:
                artist = Artist.objects.get(pk=pk)

                if request.user.favourite_artists.filter(pk=pk).exists():
                    request.user.favourite_artists.remove(artist)
                else:
                    request.user.favourite_artists.add(artist)
            except Artist.DoesNotExist:
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
                    f'<a class="user" href="/user/{activity.user.id}">{activity.user.username}</a>'
                )
                song_html = (
                    f'<a class="song" href="/song/{ activity.song.id }">{ activity.song.title }</a>'
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
                    <div class="content">
                        {user_html}
                        <p class="text">{text_html}</p>
                        <img class="avatar" src="" alt="">
                    </div>
                
                </div>"""

                activites_html += html

            context = {"activities": activites_html}

            return render(request, self.template_name_logged, context)

        return render(request, self.template_name)


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
