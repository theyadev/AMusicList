from django.urls import path

from . import views

urlpatterns = [
    path("", views.MainView.as_view()),
    path("song/<int:pk>/", views.SongView.as_view(), name="song"),
    path("artist/<int:pk>/", views.ArtistView.as_view(), name="artist"),
    path("album/<int:pk>/", views.AlbumView.as_view(), name="album"),
    path('songs', views.SongsView.as_view(), name="songs"),
    path('artists', views.ArtistsView.as_view(), name="artists"),
    path('albums', views.AlbumsView.as_view(), name="albums"),
]
