from django.urls import path

from . import views

urlpatterns = [
    path("user/<int:pk>/", views.UserView.as_view(), name="user"),
]
