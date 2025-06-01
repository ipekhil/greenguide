import requests
from plants.models import PlantType

API_KEY = "sk-YSU368346c483027310667"
API_URL = f"https://perenual.com/api/species-list?key={API_KEY}&page=1"

response = requests.get(API_URL)
data = response.json()

for plant in data.get("data", []):
    name = plant.get("common_name") or plant.get("scientific_name")

    if not name or PlantType.objects.filter(name=name).exists():
        continue

    # Işık tercihi
    sunlight = plant.get("sunlight", [])
    if sunlight and isinstance(sunlight, list):
        if "full_sun" in sunlight:
            light = "Full Sun"
        elif "partial_shade" in sunlight:
            light = "Partial Shade"
        elif "shade" in sunlight:
            light = "Shade"
        else:
            light = "Unknown"
    else:
        light = "Unknown"

    # İsim kontrollü sulama ve gübreleme önerisi
    lower_name = name.lower() if name else ""
    if "fir" in lower_name:
        watering = 10
        fertilizing = 90
    elif "maple" in lower_name:
        watering = 7
        fertilizing = 60
    elif "succulent" in lower_name:
        watering = 14
        fertilizing = 120
    else:
        watering = 7
        fertilizing = 45

    PlantType.objects.create(
        name=name,
        info=plant.get("description", "") or "No description available.",
        watering_frequency=watering,
        fertilizing_frequency=fertilizing,
        light_preference=light,
        ideal_temperature= 22
    )

    print(f"✅ Added: {name}")
