from django.contrib import admin
from .models import Cafe
from .models import Coordinates
from .models import OpeningHours
from .models import Owner
from .models import Item
from django.contrib.auth.admin import UserAdmin

admin.site.register(Cafe)
admin.site.register(Coordinates)
admin.site.register(OpeningHours)
admin.site.register(Owner)
admin.site.register(Item)


class SomeModelAdmin(admin.ModelAdmin):
    raw_id_fields = ("cafe_menu",)
