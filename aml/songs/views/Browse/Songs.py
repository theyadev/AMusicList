from django.db.models import Q

from .Base import BrowseView

from ...models import Song


class SongsView(BrowseView):
    """Browse page for songs"""

    model = Song
    name = "Musiques"
    options = """
        <option value="title">Titre</option>
        <option value="id">id</option>
        <option value="artists__name">Artiste</option>
    """
    active = "songs"

    def filter_queryset(self):
        filter_val = self.request.GET.get("search", "")

        queryset = self.model.objects.filter(
            Q(title__icontains=filter_val) | Q(artists__name__icontains=filter_val)
        )

        return queryset

    def get_data(self, item):
        return item.id, item.imageUrl, item.title
