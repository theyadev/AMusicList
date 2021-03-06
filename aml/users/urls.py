from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("login", views.LoginView.as_view(), name="login"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("user/<int:pk>/", views.UserView.as_view(), name="user"),
    path("user/<int:pk>/edit", views.SettingsView.as_view(), name="settings"),
    path("api/add/<int:songId>", views.AddToListView.as_view()),
    path("api/add/favourite/<int:songId>", views.AddToFavourite.as_view()),
    path("api/notifications/<int:notificationId>", views.NotificationView.as_view()),
    path("api/notifications/all", views.NotificationAllView.as_view()),
]
