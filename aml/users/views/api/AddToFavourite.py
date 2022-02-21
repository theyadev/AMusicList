from django.shortcuts import redirect, render
from django.urls import reverse
from ...models import Lists, Activities
from django.views import View

from songs.models import Song


class AddToFavourite(View):
    """Endpoint to add a song to favourite"""

    def post(self, request, songId):
        if request.user.is_authenticated:
            try:
                song = Song.objects.get(id=songId)
            except Song.DoesNotExist:
                return render(request, "404.html")

            try:
                list_entry = Lists.objects.get(user=request.user, song=song)
                list_entry.favourite = not list_entry.favourite

                if list_entry.favourite:
                    action = "ADDED FAVOURITE"
                else:
                    action = "REMOVED FAVOURITE"

                list_entry.save()

                activity = Activities(song=song, user=request.user, action=action)
                activity.save()
            except:
                return redirect(reverse("song", args=[songId]))

        return redirect(reverse("song", args=[songId]))
