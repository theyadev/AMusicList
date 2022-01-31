from django.urls import path

from .views import views
from .views import api

urlpatterns = [
    path("", views.MainView.as_view()),
    path("login", views.LoginView.as_view()),
    path("signup", views.SignupView.as_view()),
    path("song/<int:pk>/", views.SongView.as_view(), name="song"),
    path("artist/<int:pk>/", views.ArtistView.as_view(), name="artist"),
    path("album/<int:pk>/", views.AlbumView.as_view(), name="album"),
    path("logout", views.LogoutView.as_view()),
    path("api/add/<int:songId>", api.AddToListView.as_view()),
    path("api/add/favourite/<int:songId>", api.AddToFavourite.as_view()),
    path('songs', views.SongsView.as_view(), name="songs"),
    path('artists', views.ArtistsView.as_view(), name="artists"),
    path('albums', views.AlbumsView.as_view(), name="albums"),
]
