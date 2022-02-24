from django.shortcuts import redirect, render
from django.views import View
from ...models import Activities, Notifications

from main.lib.utils import getRedirect


class NotificationView(View):
    """Endpoint to archive a notification"""

    def post(self, request, notificationId):
        if request.user.is_authenticated:
            try:
                notif = Notifications.objects.get(id=notificationId)
            except Activities.DoesNotExist:
                return render(request, "404.html")

            notif.archived = True
            notif.save()

        return redirect(getRedirect(request))

class NotificationAllView(View):
    """Endpoint to archive all notifications"""

    def post(self, request):
        if request.user.is_authenticated:
            for notif in request.user.notifs.all():
                notif.archived = True
                notif.save()

        return redirect(getRedirect(request))
