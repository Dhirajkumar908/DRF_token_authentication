from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display=['car_brand','car_model', 'engin_type']
