from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView
from ..models import Artist


class ArtistView(DetailView):
    """
    Single artist view.
    Can add an artist to favourite on this page
    """

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
