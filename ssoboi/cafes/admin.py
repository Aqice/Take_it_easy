from django.contrib import admin
from .models import Cafe
from .models import Coordinates
from .models import OpeningHours
from .models import Owner
from .models import Item
from .models import WaitList


class CafeListAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'add_time']
    list_display_links = ['add_time', '__str__']
    list_filter = ['add_time']
    search_fields = ['cafe_name']
    filter_horizontal = ['cafe_menu']


class WaitListAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'time_to_take', 'cafe_id']
    list_display_links = ['time_to_take', '__str__', 'cafe_id']
    list_filter = ['time_to_take', 'order_id']


admin.site.register(WaitList, WaitListAdmin)
admin.site.register(Cafe, CafeListAdmin)
admin.site.register(Coordinates)
admin.site.register(OpeningHours)
admin.site.register(Owner)
admin.site.register(Item)
