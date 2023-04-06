from django.forms import ModelForm,TextInput
from .models import City

class CityName (ModelForm):
    class Meta:
        model = City
        fields =[ "name"]
        widgets ={'name':TextInput(attrs={'class':'form-control','placeholder':'Enter City Name'})}