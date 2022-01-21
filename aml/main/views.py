from django.http import HttpResponse
from django.shortcuts import render

from .models import Song

def index(request):
    return HttpResponse("Hello, world. You're at the main index.")

def detail(request, songId):
    try:
        song = Song.objects.get(id=songId)
    except Song.DoesNotExist:
        return render(request, "main/404.html")

    context = {'song': song}

    return render(request, 'main/detail.html', context)

def staff(request, songId):
    return HttpResponse("Staff de la musique: %s" % songId)