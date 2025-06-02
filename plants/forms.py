from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PlantType
from .models import UserPlant
from datetime import date
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
            'last_watered': forms.DateInput(attrs={
                'type': 'date',
                'max': date.today().isoformat()
            }),
            'last_fertilized': forms.DateInput(attrs={
                'type': 'date',
                'max': date.today().isoformat()
            }),
        }
    def clean_last_watered(self):
        last_watered = self.cleaned_data.get('last_watered')
        if last_watered and last_watered > date.today():
            raise forms.ValidationError("Last watered date cannot be in the future.")
        return last_watered

    def clean_last_fertilized(self):
        last_fertilized = self.cleaned_data.get('last_fertilized')
        if last_fertilized and last_fertilized > date.today():
            raise forms.ValidationError("Last fertilized date cannot be in the future.")
        return last_fertilized