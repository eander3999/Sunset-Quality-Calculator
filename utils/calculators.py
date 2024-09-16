from abc import ABC, abstractmethod
import numpy as np

class SunsetQualityCalculator(ABC):
    @abstractmethod
    def calculate_sunset_quality(self):
        pass

class SimpleSunsetQualityCalculator(SunsetQualityCalculator):
    def calculate_sunset_quality(self, clouds, humidity, wind_speed, air_quality, description):
        """
        Calculate the sunset quality index using a weighted formula based on clouds, humidity, wind speed, 
        air quality, and the weather description.

        Args:
            clouds (int): Cloud coverage percentage (0-100).
            humidity (int): Humidity percentage (0-100).
            wind_speed (float): Wind speed in meters per second.
            air_quality (int): Air quality index (1-5).
            description (str): Weather description (e.g., "clear sky", "few clouds", etc.).

        Returns:
            float: Sunset quality index (0-10).
        """
        cloud_score = self.__calculate_cloud_score(clouds, description)
        humidity_score = 1 - (humidity / 100)
        wind_score = max(0, 1 - (wind_speed / 10))
        air_quality_score = self.__calculate_air_quality(air_quality)
        sqi = 10 * (0.7 * cloud_score + 0.1 * humidity_score + 0.1 * wind_score + 0.1 * air_quality_score)
        print(f"DEBUG: cloud score={cloud_score}, humidity_score={humidity_score}, wind_score={wind_score}, air_quality_score={air_quality_score}")
        return round(sqi, 1)

    def __calculate_cloud_score(self, clouds, description):
        """
        Calculate the cloud score based on cloud coverage and weather description.

        Args:
            clouds (int): Cloud coverage percentage (0-100).
            description (str): Weather description (e.g., "clear sky", "few clouds", etc.).

        Returns:
            float: Cloud score (0-1)
        """
        description_scores = {
        "clear sky": 0.25,
        "few clouds": 0.5,
        "scattered clouds": 1,
        "broken clouds": 0.75 if clouds < 60 else 0.25,
    }
        score = description_scores.get(description, 0)
        return score
    
    def __calculate_air_quality(self, air_quality):
        """
        Calculate the air quality score based on the air quality index (AQI).
        Note: Poor air quality leads to more vibrant sunsets

        Args:
            air_quality (int): Air quality index (1-5), where 1 is good and 5 is hazardous.

        Returns:
            float: Air quality score (0-1), where higher values indicate better air quality for vibrant sunsets.
        """
        air_quality_scores = {
        1: 0.5,
        2: 0.6,
        3: 0.75,
        4: 0.9,
        5: 1,
        }
        score = air_quality_scores.get(air_quality, 0)
        return score
