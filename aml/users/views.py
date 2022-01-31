from django.shortcuts import redirect, render
from django.views.generic import DetailView
from django.urls import reverse
from .models import User


class UserView(DetailView):
    template_name = "user.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user
        context["is_following"] = (
            self.get_object().user_followers.filter(id=self.request.user.id).exists()
        )

        return context

    def post(self, request, pk):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=pk)

                if request.user.follows.filter(pk=pk).exists():
                    request.user.follows.remove(user)
                else:
                    request.user.follows.add(user)
            except:
                pass

        return redirect(reverse("user", args=[pk]))
