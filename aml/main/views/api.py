from django.shortcuts import redirect, render
from django.views import View

from ..models import Song, User, Lists, Activities


class AddToListView(View):
    def post(self, request, songId):
        if request.user.is_authenticated:
            try:
                song = Song.objects.get(id=songId)
            except Song.DoesNotExist:
                return render(request, "404.html")

            try:
                list_entry = Lists.objects.get(user=request.user, song=song)
                list_entry.delete()
                action = "REMOVED"
            except:
                list_entry = Lists(user=request.user, song=song, favourite=False)
                list_entry.save()
                action = "ADDED"

            activity = Activities(song=song, user=request.user, action=action)
            activity.save()

        return redirect("/song/" + str(songId))

class AddToFavourite(View):
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
                return redirect("/song/" + str(songId))

        return redirect("/song/" + str(songId))
