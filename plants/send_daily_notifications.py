import os
import django
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenguide.settings")
django.setup()

from plants.models import UserPlant
from django.core.mail import send_mail

today = date.today()

user_plants = UserPlant.objects.select_related('plant_type', 'user').all()

water_reminders = []
fertilize_reminders = []

for plant in user_plants:
    user = plant.user
    email = user.email
    name = plant.nickname or plant.plant_type.name

    if not email:
        continue

    messages = []

    if plant.next_water_date() == today:
        messages.append(f"💧 Water your plant: {name}")
        water_reminders.append(name)

    if plant.next_fertilize_date() == today:
        messages.append(f"🌿 Fertilize your plant: {name}")
        fertilize_reminders.append(name)

    if messages:
        send_mail(
            subject="Green Guide – Today's Plant Care Reminder 🌱",
            message="\n".join(messages),
            from_email="info@greenguide.com.tr",
            recipient_list=[email],
            fail_silently=False,
        )

print(f"Sent {len(water_reminders)} watering and {len(fertilize_reminders)} fertilizing reminders.")
