from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  User,  Activities, Lists
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Activities)
admin.site.register(Lists)