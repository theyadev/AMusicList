from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from ..forms import SettingsForm, SettingsPasswordForm

from django.views import View


class SettingsView(View):
    """Settingd view"""

    template_name = "users/settings.html"

    def get_context_data(self, **kwargs):
        context = {}

        context["form"] = SettingsForm(instance=self.request.user)
        context["password_form"] = SettingsPasswordForm

        return context

    def get(self, request, *args, **kwargs):
        if request.user.id != kwargs["pk"]:
            return redirect("/")

        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.user.id != kwargs["pk"]:
            return redirect("/")

        form = SettingsForm(request.POST, request.FILES, instance=self.request.user)
        password_form = SettingsPasswordForm(request.POST)

        if form.is_valid():
            user = form.save()

            return redirect(reverse("user", args=[user.id]))

        if password_form.is_valid(request.user):
            user = password_form.save(request.user)
            update_session_auth_hash(request, user)

            return redirect(reverse("user", args=[user.id]))

        return render(request, self.template_name, self.get_context_data())
