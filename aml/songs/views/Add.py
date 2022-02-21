from django.shortcuts import redirect, render
from django.views.generic import FormView

from ..forms import AddForm
from ..models import Album, Song, Artist

from main.lib.spotipy import (
    sp,
    importTracksFromAlbum,
    importAlbumFromTrack,
    importAlbumsFromPlaylist,
)


class AddView(FormView):
    """View to add songs/albums/playlist"""

    template_name = "songs/add.html"
    form_class = AddForm

    def handle_form(self, get):
        query = get.get("query")
        type = get.get("type")
        csrf = get.get("csrfmiddlewaretoken")

        if query is None or type is None:
            return None, None, None

        if query == "":
            return None, None, None

        result = sp.search(query, type=type)

        return result[type + "s"]["items"], type + "s", csrf

    def generate_cards(self, list, type, csrf):
        cards = ""

        for item in list:
            if Song.objects.filter(spotifyId=item["id"]).exists():
                continue
            if Artist.objects.filter(spotifyId=item["id"]).exists():
                continue
            if Album.objects.filter(spotifyId=item["id"]).exists():
                continue

            card = f"""
            <div>{item['name']}</div>
            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf}">
                <input type="hidden" name="id" value="{item['id']}">
                <input type="hidden" name="type" value="{type}">
                <button>Ajouter</button>
            </form>
            """

            cards += card

        return cards

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/")

        if (
            request.user.is_superuser == False
            and not request.user.user_permissions.all()
            .filter(name="Can add song")
            .exists()
        ):
            return redirect("/")

        context = self.get_context_data()

        query_list, query_type, csrf = self.handle_form(request.GET)

        if query_list is not None:
            cards = self.generate_cards(query_list, query_type, csrf)
            context["cards"] = cards

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_data = request.POST

        id = form_data["id"]
        type = form_data["type"]

        if type == "albums":
            importTracksFromAlbum(id)

        elif type == "tracks":
            importAlbumFromTrack(id)

        elif type == "playlists":
            importAlbumsFromPlaylist(id)

        return redirect("add")
