from django.urls import path

from .views import views
from .views import api

urlpatterns = [
    path("", views.MainView.as_view()),
    path("login", views.LoginView.as_view()),
    path("signup", views.SignupView.as_view()),
    path("user/<int:pk>/", views.UserView.as_view()),
    path("song/<int:pk>/", views.SongView.as_view()),
    path("artist/<int:pk>/", views.ArtistView.as_view()),
    path("album/<int:pk>/", views.AlbumView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("api/add/<int:songId>", api.add_to_list),
    path("api/add/favourite/<int:songId>", api.add_to_favourite),
    path("api/addfriend", api.add_friend),
]
