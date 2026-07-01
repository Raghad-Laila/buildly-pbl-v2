from django.contrib import admin
from .models import CustomUser, UserFavorite

admin.site.register(CustomUser)
admin.site.register(UserFavorite)
