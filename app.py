from flask import Flask, request, jsonify, render_template, url_for, redirect
from utils.weather_fetcher import WeatherDataFetcher
from utils.calculators import SimpleSunsetQualityCalculator
from utils.location_converter import get_location_details
import joblib

app = Flask(__name__)

simple_calculator = SimpleSunsetQualityCalculator()

api_key = '894a6f326dd01eaff5b9193b89be985e'
weather_fetcher = WeatherDataFetcher(api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def predict_sunset():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({'error': 'Location not provided'}), 400
    lat, lon, formatted_location = get_location_details(zip_code, api_key)
    if lat is None or lon is None:
        return jsonify({'error': 'Could not find location'}), 400
    try:
        weather_data = weather_fetcher.get_current_and_forecast_data(lat, lon)
        sunset_timestamp = weather_fetcher.get_sunset_time(weather_data)
        air_quality_data = weather_fetcher.get_air_quality_data(lat, lon)
        air_quality = weather_fetcher.extract_air_quality_index(air_quality_data, sunset_timestamp)
        clouds, humidity, wind_speed, description = weather_fetcher.extract_relevant_data(weather_data, sunset_timestamp)
        sqi_simple = simple_calculator.calculate_sunset_quality(clouds, humidity, wind_speed, air_quality, description)
        return jsonify({'location': formatted_location, 'sunset_quality_index_simple': sqi_simple})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
