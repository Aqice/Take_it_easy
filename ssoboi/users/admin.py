from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ['groups']


admin.site.register(User, UserAdmin)

