from django.db.models import Q

from .Base import BrowseView

from ...models import Album


class AlbumsView(BrowseView):
    """Browse page for albums"""

    model = Album
    name = "Albums"
    active = "albums"

    def filter_queryset(self):
        filter_val = self.request.GET.get("search", "")

        queryset = self.model.objects.filter(
            Q(name__icontains=filter_val) | Q(artists__name__icontains=filter_val)
        )

        return queryset
