import requests

def get_location_details(zip_code, api_key):
    """
    Convert a ZIP code into latitude, longitude, and a formatted location string.

    Args:
        zip_code (str): The ZIP code input by the user.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        tuple: A tuple containing latitude, longitude, and a formatted location string,
               or (None, None, None) if not found.
    """
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200 or not response.json():
        return None, None, None 
    
    data = response.json()
    
    lat = data.get('lat', None)
    lon = data.get('lon', None)
    city = data.get('name', '')
    country = data.get('country', '')

    location_string = f"{city}, {country}"
    
    return lat, lon, location_string
