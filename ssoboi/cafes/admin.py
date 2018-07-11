from django.contrib import admin
from .models import Cafe
from .models import Coordinates
from .models import OpeningHours
from .models import Owner
from .models import Item
from django.contrib.auth.admin import UserAdmin


class CafeListAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'add_time']
    list_display_links = ['add_time', '__str__']
    list_filter = ['add_time']
    search_fields = ['cafe_name']
    filter_horizontal = ['cafe_menu']


admin.site.register(Cafe, CafeListAdmin)
admin.site.register(Coordinates)
admin.site.register(OpeningHours)
admin.site.register(Owner)
admin.site.register(Item)