from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('song/<int:songId>', views.detail, name="detail"),
    path('staff/<int:staffId>', views.staff, name="staff"),
    path('logout', views.logout_view, name="logout"),
    path('login', views.login_view, name="Login"),
    path('signup', views.signup_view, name="Sign Up")
]