from django.shortcuts import render
import urllib.parse
import urllib.request
import json
from django.contrib import messages
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        encoded_city = urllib.parse.quote(city)
        url = f'http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&units=metric&appid={API_KEY}'

        try:
            source = urllib.request.urlopen(url).read()
            list_of_data = json.loads(source)
            
            data = {
                "country_code" : str(list_of_data['sys']['country']),
                "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                "temp": str(list_of_data['main']['temp']) + ' °C',
                "pressure": str(list_of_data['main']['pressure']),
                "humidity": str(list_of_data['main']['humidity']),
                "main": str(list_of_data['weather'][0]['main']),
                "description":  str(list_of_data['weather'][0]['description']),
                "icon": list_of_data['weather'][0]['icon'],
            }

            print(data)
        except urllib.error.HTTPError as e:
            error_message = e.read().decode('utf-8')
            print(f"HTTP Error occurred: {error_message}")
            messages.error(request, f"Error occurred: {error_message}")
            data = {}
    else:
        data = {}
       
    return render(request, "main/index.html", {"data": data})
