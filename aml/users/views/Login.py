from django.shortcuts import redirect, render
from django.views.generic import FormView
from django.contrib.auth import login
from ..forms import LoginForm


from songs.models import Artist

from random import choice

from main.lib.utils import getRedirect


class LoginView(FormView):
    """Login view"""

    template_name = "users/login.html"
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        artists = Artist.objects.exclude(imageUrl="")

        context = {"form": self.form_class(), "artist": choice(artists.all())}
        print(context)
        return context

    def get(self, request, *args, **kwargs):
        redirect_url = getRedirect(self.request)

        if request.user.is_authenticated:
            return redirect(redirect_url)

        return render(request, self.template_name, self.get_context_data())

    def form_valid(self, form):
        user = form.get_user(self.request)

        print(user)

        if user is not None:
            login(self.request, user)

            redirect_url = getRedirect(self.request)
            return redirect(redirect_url)

        return redirect(self.request.get_full_path())

    def form_invalid(self, form):
        print(form.errors)
        print(self.request.FILES)
        return super().form_invalid(form)
