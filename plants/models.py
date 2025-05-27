from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

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


class UserPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, help_text="Give your plant a name!")

    last_watered = models.DateField(default=date.today)
    last_fertilized = models.DateField(default=date.today)

    def next_water_date(self):
        next_date = self.last_watered
        while next_date <= date.today():
            next_date += timedelta(days=self.plant_type.watering_frequency)
        return next_date

    def next_fertilize_date(self):
        next_date = self.last_fertilized
        while next_date <= date.today():
            next_date += timedelta(days=self.plant_type.fertilizing_frequency)
        return next_date

    def __str__(self):
        return f"{self.nickname} ({self.plant_type.name})"

