from django.db.models import Q

from .Base import BrowseView

from ...models import Artist


class ArtistsView(BrowseView):
    """Browse page for artists"""

    model = Artist
    name = "Artistes"
    active = "artists"

    def filter_queryset(self):
        filter_val = self.request.GET.get("search", "")

        queryset = self.model.objects.filter(name__icontains=filter_val)

        return queryset
