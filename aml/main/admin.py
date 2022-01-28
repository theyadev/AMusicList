from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Album, Artist, Song, User, Lists, Activities; Album

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Lists)
admin.site.register(Activities)
