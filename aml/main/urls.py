from django.urls import path

from .views import views
from .views import api

urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("signup", views.signup),
    path("api/logout", api.logout_api),
    path("api/signup", api.signup_api),
    path("api/login", api.login_api),
    path("api/add/<int:songId>", api.add_to_list),
    path("api/add/favourite/<int:songId>", api.add_to_favourite),
    path("api/addfriend", api.add_friend),
    path("user/<int:pk>/", views.UserView.as_view()),
    path("song/<int:pk>/", views.SongView.as_view()),
    path("artist/<int:pk>/", views.ArtistView.as_view()),
    path("album/<int:pk>/", views.AlbumView.as_view()),
]
