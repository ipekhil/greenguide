import requests
from plants.models import PlantType

API_KEY = "sk-YSU368346c483027310667"
url = f"https://perenual.com/api/species-list?key={API_KEY}&page=1"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    for plant in data.get("data", []):
        name = plant.get("common_name", "Unknown")
        info = plant.get("description", "") or "No info."
        watering_text = (plant.get("watering") or "").lower()
        light_list = plant.get("sunlight", [])
        light = ", ".join(light_list) if light_list else "Unknown"

        # Sulama → gübreleme frekansını tahmini belirle
        if "frequent" in watering_text:
            watering_frequency = 3
            fertilizing_frequency = 15
        elif "average" in watering_text:
            watering_frequency = 7
            fertilizing_frequency = 30
        elif "minimum" in watering_text or "low" in watering_text:
            watering_frequency = 14
            fertilizing_frequency = 45
        else:
            watering_frequency = 10
            fertilizing_frequency = 30

        ideal_temperature = 20  # API'de olmadığından örnek değer

        obj, created = PlantType.objects.get_or_create(
            name=name,
            defaults={
                'info': info,
                'watering_frequency': watering_frequency,
                'fertilizing_frequency': fertilizing_frequency,
                'light_preference': light,
                'ideal_temperature': ideal_temperature
            }
        )

        if created:
            print(f"✅ Added: {name}")
        else:
            print(f"↪️ Skipped (already exists): {name}")
else:
    print("HATA:", response.status_code)
