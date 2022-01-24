from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff, Song, UserRole, User, Lists

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(Staff)
admin.site.register(Song)
admin.site.register(UserRole)
admin.site.register(Lists)
