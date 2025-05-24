from django.db import models

# Create your models here.
class PlantType(models.Model):
    name = models.CharField(max_length=100)
    info = models.TextField()
    watering_frequency = models.PositiveIntegerField(help_text="Irrigation frequency (day)")
    fertilizing_frequency = models.PositiveIntegerField(help_text="Fertilization frequency (days)")
    light_preference = models.CharField(max_length=100)
    ideal_temperature = models.IntegerField(help_text="Ideal temperature (°C)")

    def __str__(self):
        return self.name