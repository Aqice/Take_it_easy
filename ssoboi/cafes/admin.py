from django.contrib import admin
from .models import Cafe
from .models import Coordinates
from .models import OpeningHours
from .models import Owner

admin.site.register(Cafe)
admin.site.register(Coordinates)
admin.site.register(OpeningHours)
admin.site.register(Owner)
