from django.views.generic import DetailView
from ..models import Album


class AlbumView(DetailView):
    """Single album view"""

    template_name = "songs/album.html"

    model = Album
