import requests

class WeatherDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_and_forecast_data(self, lat, lon):
        """
        Fetch 5-day/3-hour forecast weather data for a given location.

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.

        Returns:
            dict: Weather data including 3-hour forecasts.
        """
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Error fetching weather data")
        data = response.json()
        return data
    
    def get_air_quality_data(self, lat, lon):
        """
        Fetch air quality data for a given location.

        Args:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.

        Returns:
            dict: Air quality data.
        """
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Error fetching air quality data")
        data = response.json()
        return data
    
    def extract_air_quality_index(self, air_quality_data, sunset_timestamp):
        """
        Extract the air quality index (AQI) closest to the sunset time from the air quality forecast data.

        Args:
            air_quality_data (dict): The air quality data retrieved from the OpenWeather API.
            sunset_timestamp (int): The Unix timestamp for the sunset time.

        Returns:
            int: The air quality index (AQI) value for the forecast closest to the sunset time.
        """
        closest_forecast = None
        min_diff = float('inf')

        for forecast in air_quality_data.get('list', []):
            forecast_time = forecast.get('dt')
            diff = abs(forecast_time - sunset_timestamp)
            if diff < min_diff:
                min_diff = diff
                closest_forecast = forecast

        if closest_forecast is None:
            raise Exception("No forecast data available close to sunset time")
        
        aqi = closest_forecast.get('main', {}).get('aqi', 0)

        print(f"DEBUG: aqi={aqi}")

        return aqi
    
    def get_sunset_time(self, weather_data):
        """
        Extract the sunset time from the weather forecast data.

        Args:
            weather_data (dict): Weather data containing city information with sunset time.

        Returns:
            int: Unix timestamp for the sunset time today.
        """
        city_info = weather_data.get('city', {})
        sunset_timestamp = city_info.get('sunset')
        if sunset_timestamp is None:
            raise Exception("Sunset time not found in the city data")
        return sunset_timestamp

    def extract_relevant_data(self, weather_data, sunset_timestamp):
        """
        Extract relevant data from the 3-hour forecast closest to the sunset time.

        Args:
            weather_data (dict): Weather data containing 3-hour forecasts.
            sunset_timestamp (int): Unix timestamp for the sunset time.

        Returns:
            tuple: (clouds, humidity, wind_speed, description)
        """
        closest_forecast = None
        min_diff = float('inf')

        for forecast in weather_data.get('list', []):
            forecast_time = forecast.get('dt')
            diff = abs(forecast_time - sunset_timestamp)
            if diff < min_diff:
                min_diff = diff
                closest_forecast = forecast

        if closest_forecast is None:
            raise Exception("No forecast data available close to sunset time")

        clouds = closest_forecast.get('clouds', {}).get('all', 0)
        humidity = closest_forecast.get('main', {}).get('humidity', 0)
        wind_speed = closest_forecast.get('wind', {}).get('speed', 0)
        description = closest_forecast.get('weather', [{}])[0].get('description', '')

        print(f"DEBUG: clouds={clouds}, humidity={humidity}, wind_speed={wind_speed}, description={description}")  # Debugging line

        return clouds, humidity, wind_speed, description
