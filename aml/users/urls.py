from django.urls import path

from . import views

urlpatterns = [
    path("user/<int:pk>/", views.UserView.as_view(), name="user"),
    path("login", views.LoginView.as_view()),
    path("signup", views.SignupView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("api/add/<int:songId>", views.AddToListView.as_view()),
    path("api/add/favourite/<int:songId>", views.AddToFavourite.as_view()),
]
