from django.shortcuts import render, redirect
from .forms import CityName
from .models import City
from django.contrib import messages
import requests

def weather(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=f9dd980d2bc1e35f5f6eaa283fc7d42c&units=metric'  
    if request.method=='POST':
        form = CityName(request.POST)
        if form.is_valid():
            cityN = form.cleaned_data["name"]
            CityNcount = City.objects.filter(name=cityN).count()
            if CityNcount == 0:
                result = requests.get(url.format(cityN)).json()
                print(result)
                if result['cod'] == 200:
                    form.save()
                    messages.success(request, cityN+" added successfully!")
                else:
                    messages.error(request, "City does not exists...")  
            else:
                messages.error(request, "City name already exists...")
    form = CityName()
    cities = City.objects.all()
    data = []
    for city in cities:
        res = requests.get(url.format(city)).json()
        cityData ={
            'city':city,
            'temperature':res['main']['temp'],
            'description': res['weather'][0]['description'],
            'country': res['sys']['country'],
            'latitude': res['coord']['lat'],
            'longtitude': res['coord']['lon'],
            'icon': res['weather'][0]['icon'],
        }
        data.append(cityData)

    return render (request, 'weather.html',{'data':data,'form':form})

def delete(request,city):
    City.objects.get(name=city).delete()
    messages.success(request, city+" deleted successfully!")
    return redirect('home')
