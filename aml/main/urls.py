from django.urls import path

from .views import views
from .views import api

urlpatterns = [
    path("", views.index, name="index"),
    path("user/<int:userId>", views.user, name="user"),
    path("song/<int:songId>", views.song, name="detail"),
    path("artist/<int:staffId>", views.artist, name="staff"),
    path("login", views.login, name="Login"),
    path("signup", views.signup, name="Sign Up"),
    path("api/logout", api.logout_api, name="logout"),
    path("api/signup", api.signup_api, name="signup"),
    path("api/login", api.login_api, name="login"),
    path("api/add/<int:songId>", api.add_to_list, name="Add song to list"),
    path("api/add/favourite/<int:songId>", api.add_to_favourite, name="Add song to fav"),

]
