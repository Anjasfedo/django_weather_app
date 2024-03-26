from django.shortcuts import render
import json
import urllib.request
from urllib.parse import quote

# Create your views here.

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        encoded_city = quote(city)
        
        try:
            res = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid=cb771e45ac79a4e8e2205c0ce66ff633').read()
            json_data = json.loads(res)
            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon']) + ' ' +
                str(json_data['coord']['lat']),
                "temp": str(json_data['main']['temp'])+'k',
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
            }
            
        except urllib.error.HTTPError as e:
            # Handle HTTP errors
            error_message = f"HTTP Error: {e.code} - {e.reason}"
            data = {'error': error_message}
            
        except urllib.error.URLError as e:
            # Handle URL errors
            error_message = f"URL Error: {e.reason}"
            data = {'error': error_message}
            
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            error_message = f"JSON Decode Error: {str(e)}"
            data = {'error': error_message}
            
        context = {
            'city': city, 
            'data': data
            }
    
        return render(request, 'htmx/result.html', context)
    
    return render(request, 'index.html')
