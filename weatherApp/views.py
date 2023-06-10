from django.shortcuts import render
import urllib.parse
import urllib.request
import json
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

            if list_of_data['cod'] == 200:
                data = {
                    "country_code": str(list_of_data['sys']['country']),
                    "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
                    "temp": str(list_of_data['main']['temp']) + ' °C',
                    "pressure": str(list_of_data['main']['pressure']),
                    "humidity": str(list_of_data['main']['humidity']),
                    "main": str(list_of_data['weather'][0]['main']),
                    "description": str(list_of_data['weather'][0]['description']),
                    "icon": list_of_data['weather'][0]['icon'],
                }
                error_message = None
            else:
                data = {}
                error_message = f"No information found for '{city}'. Please enter a valid city or country."

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"City not found: {city}")
                data = {}
                error_message = f"No weather information found for '{city}'. Please enter a valid city or country."
            else:
                print(f"HTTP Error: {e}")
                data = {}
                error_message = "Sorry, an error occurred while retrieving weather information."
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            data = {}
            error_message = "Sorry, an error occurred while retrieving weather information."

    else:
        data = {}
        error_message = None

    return render(request, "main/index.html", {"data": data, "error_message": error_message})
