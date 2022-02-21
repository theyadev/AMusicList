from django.views.generic import DetailView

from ..models import Song

from users.models import Lists


class SongView(DetailView):
    """Single song view"""

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
