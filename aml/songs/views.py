from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse
from django.views.generic import DetailView, ListView
from .models import Album, Song, Artist

from users.models import Activities, Lists


class BrowseView(ListView):
    """
    Render the browse page with desired model
    """

    model = None
    template_name = "songs/browse.html"
    paginate_by = 100
    name = None
    options = """
        <option value="name">Nom</option>
        <option value="id">id</option>
    """

    def filter_queryset(self):
        return self.model.objects

    def get_queryset(self):
        order_val = self.request.GET.get("order", "id")

        queryset = self.filter_queryset().order_by(order_val).distinct(order_val)

        return queryset

    def get_data(self, item):
        """
        Returns data to fill the card.

        Needs to return id, image_link and a name
        """

        return item.id, item.imageUrl, item.name

    def get_cards(self):
        cards = ""
        for item in self.paginate_queryset(self.get_queryset(), self.paginate_by)[2]:
            id, image_url, name = self.get_data(item)
            card = f"""
            <div style="margin: 0 5px">
                <a href="{reverse(self.model.__name__.lower(), args=[id])}">
                    <img style="width:10rem" src="{image_url}" alt="{name}">
                    <p style="text-align:center;text-overflow: ellipsis;overflow: hidden;white-space: nowrap;width:17ch">
                        {name}</p>
                </a>
            </div>
            """

            cards += card
        return cards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        context["order"] = self.request.GET.get("order", "title")
        context["cards"] = self.get_cards()
        context["name"] = self.name

        get_copy = self.request.GET.copy()

        if get_copy.get("page"):
            get_copy.pop("page")

        context["get_copy"] = get_copy

        return context


# Create your views here.
class SongView(DetailView):
    template_name = "songs/song.html"
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
    template_name = "songs/artist.html"

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
    template_name = "songs/album.html"

    model = Album


class SongsView(BrowseView):
    model = Song
    name = "Musiques"
    options = """
        <option value="title">Titre</option>
        <option value="id">id</option>
        <option value="artists__name">Artiste</option>
    """

    def filter_queryset(self):
        filter_val = self.request.GET.get("search", "")

        queryset = self.model.objects.filter(
            Q(title__icontains=filter_val) | Q(artists__name__icontains=filter_val)
        )

        return queryset

    def get_data(self, item):
        return item.id, item.imageUrl, item.title


class ArtistsView(BrowseView):
    model = Artist
    name = "Artistes"

    def filter_queryset(self):
        filter_val = self.request.GET.get("search", "")

        queryset = self.model.objects.filter(name__icontains=filter_val)

        return queryset


class AlbumsView(BrowseView):
    model = Album
    name = "Albums"

    def filter_queryset(self):
        filter_val = self.request.GET.get("search", "")

        queryset = self.model.objects.filter(
            Q(name__icontains=filter_val) | Q(artists__name__icontains=filter_val)
        )

        return queryset
