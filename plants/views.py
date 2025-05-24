from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import PlantTypeForm
from .models import PlantType
from django.shortcuts import get_object_or_404

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
    return render(request, "plants/admin_dashboard.html")

@login_required
def dashboard(request):
    if request.user.is_staff:
        # admin dashboard
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
        return render(request, "plants/user_dashboard.html")

@login_required
def delete_plant_type(request, id):
    if not request.user.is_staff:
        return redirect("dashboard")

    plant = get_object_or_404(PlantType, id=id)
    plant.delete()
    return redirect("dashboard")