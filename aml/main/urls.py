from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:songId>', views.detail, name="detail"),
    path('<int:songId>/staff', views.staff, name="staff"),
]