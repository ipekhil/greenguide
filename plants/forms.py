from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PlantType
from .models import UserPlant

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PlantTypeForm(forms.ModelForm):
    class Meta:
        model = PlantType
        fields = [
            'name',
            'info',
            'watering_frequency',
            'fertilizing_frequency',
            'light_preference',
            'ideal_temperature',
        ]
        widgets = {
            'info': forms.Textarea(attrs={'rows': 3}),
        }

class UserPlantForm(forms.ModelForm):
    class Meta:
        model = UserPlant
        fields = ['plant_type', 'nickname', 'last_watered', 'last_fertilized']
        widgets = {
            'last_watered': forms.DateInput(attrs={'type': 'date'}),
            'last_fertilized': forms.DateInput(attrs={'type': 'date'}),
        }