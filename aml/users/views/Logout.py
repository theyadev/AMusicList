from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views import View

from main.lib.utils import getRedirect


class LogoutView(View):
    """Logout endpoint"""

    def get(self, request, *args, **kwargs):
        redirect_url = getRedirect(request)

        if request.user.is_authenticated:
            logout(request)

        return redirect(redirect_url)
