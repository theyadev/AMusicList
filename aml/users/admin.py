from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Activities, Lists

admin.site.register(User, UserAdmin)
admin.site.register(Activities)
admin.site.register(Lists)
