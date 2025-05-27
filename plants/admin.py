from django.contrib import admin
from .models import PlantType

@admin.register(PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'watering_frequency', 'fertilizing_frequency', 'light_preference', 'ideal_temperature')
    search_fields = ('name',)
    list_editable = ('watering_frequency', 'fertilizing_frequency', 'light_preference', 'ideal_temperature')
    list_per_page = 20

    def has_add_permission(self, request):
        return False