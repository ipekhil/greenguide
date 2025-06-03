from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import PlantTypeForm
from .models import PlantType
from .forms import UserPlantForm
from .models import UserPlant
from datetime import date
from .utils import send_plant_reminder_email
from django.core.mail import send_mail



# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "plants/register.html", {"form": form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        # Admin dashboard
        form = PlantTypeForm()

        if request.method == "POST":
            form = PlantTypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")

        plant_types = PlantType.objects.all()

        return render(request, "plants/admin_dashboard.html", {
            "form": form,
            "plant_types": plant_types
        })

    else:
        # User dashboard
        user_plants = UserPlant.objects.filter(user=request.user)

        today = date.today()

        if request.method == 'POST':
            form = UserPlantForm(request.POST)
            if form.is_valid():
                user_plant = form.save(commit=False)
                user_plant.user = request.user
                user_plant.save()
                if user_plant.next_water_date() <= today:
                    send_plant_reminder_email(request.user, user_plant, task_type="water")
                    user_plant.last_reminder_sent = today
                    user_plant.save()

                elif user_plant.next_fertilize_date() <= today:
                    send_plant_reminder_email(request.user, user_plant, task_type="fertilize")
                    user_plant.last_reminder_sent = today
                    user_plant.save()
                return redirect('dashboard')

        else:
            form = UserPlantForm()

        alerts = get_today_alerts(request.user)
        return render(request, "plants/user_dashboard.html", {
            "plants": user_plants,
            "alerts": alerts,
            "plant_form": form
        })

def get_today_alerts(user):
    today = date.today()
    alerts = []
    user_plants = UserPlant.objects.filter(user=user)

    for plant in user_plants:
        if plant.next_water_date() <= today:
            alerts.append(f"💧 Water your {plant.nickname} today!")
        if plant.next_fertilize_date() <= today:
            alerts.append(f"🌿 Fertilize your {plant.nickname} today!")
    return alerts

@login_required
def delete_plant_type(request, id):
    if not request.user.is_staff:
        return redirect("dashboard")

    plant = get_object_or_404(PlantType, id=id)
    plant.delete()
    return redirect("dashboard")


@login_required
def edit_plant_type(request, plant_id):
    plant = get_object_or_404(PlantType, id=plant_id)

    if request.method == 'POST':
        form = PlantTypeForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PlantTypeForm(instance=plant)

    return render(request, 'plants/edit_plant_type.html', {
        'form': form,
        'plant': plant
    })

@login_required
def user_plants(request):
    plants = UserPlant.objects.filter(user=request.user)
    return render(request, "plants/user_plants.html", {"plants": plants})

@login_required
def all_alerts(request):
    today = date.today()
    user_plants = UserPlant.objects.filter(user=request.user)
    alerts = []
    for plant in user_plants:
        if plant.next_water_date() <= today:
            alerts.append(f"💧 Water your {plant.nickname} today!")
        if plant.next_fertilize_date() <= today:
            alerts.append(f"🌿 Fertilize your {plant.nickname} today!")
    return render(request, "plants/alerts.html", {"alerts": alerts})

@login_required
def delete_user_plant(request, id):
    plant = get_object_or_404(UserPlant, id=id, user=request.user)
    plant.delete()
    return redirect('dashboard')


@login_required
def user_plant_detail(request, pk):
    plant = get_object_or_404(UserPlant, pk=pk, user=request.user)
    return render(request, "plants/user_plant_detail.html", {"plant": plant})

