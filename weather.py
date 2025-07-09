"""
Weather API Module for Interactive Weather App
Handles all OpenWeatherMap API interactions and data processing
"""

import requests
import json
from datetime import datetime
from typing import Dict, Optional, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherAPI:
    """
    A class to handle weather data retrieval from OpenWeatherMap API
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = os.getenv('API_BASE_URL', 'https://api.openweathermap.org/data/2.5')
        self.timeout = int(os.getenv('API_TIMEOUT', '10'))
        
        if not self.api_key or self.api_key == 'your_api_key_here':
            raise ValueError("Please set your OpenWeatherMap API key in the .env file")
    
    def get_current_weather(self, city: str, units: str = 'metric') -> Optional[Dict]:
        """
        Get current weather data for a specific city
        
        Args:
            city (str): Name of the city
            units (str): Units for temperature (metric, imperial, kelvin)
            
        Returns:
            Dict: Weather data or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Process and format the weather data
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'weather_icon': data['weather'][0]['icon'],
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'wind_direction': data.get('wind', {}).get('deg', 0),
                'visibility': data.get('visibility', 0),
                'clouds': data.get('clouds', {}).get('all', 0),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'timestamp': datetime.now()
            }
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return None
        except KeyError as e:
            print(f"Data Processing Error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None
    
    def get_forecast(self, city: str, days: int = 5, units: str = 'metric') -> Optional[List[Dict]]:
        """
        Get weather forecast for a specific city
        
        Args:
            city (str): Name of the city
            days (int): Number of days (max 5 for free API)
            units (str): Units for temperature
            
        Returns:
            List[Dict]: List of forecast data or None if error
        """
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': units,
                'cnt': days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            forecast_list = []
            for item in data['list']:
                forecast_data = {
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'weather_main': item['weather'][0]['main'],
                    'weather_description': item['weather'][0]['description'],
                    'weather_icon': item['weather'][0]['icon'],
                    'wind_speed': item.get('wind', {}).get('speed', 0),
                    'clouds': item.get('clouds', {}).get('all', 0),
                    'pop': item.get('pop', 0)  # Probability of precipitation
                }
                forecast_list.append(forecast_data)
            
            return forecast_list
            
        except requests.exceptions.RequestException as e:
            print(f"Forecast API Request Error: {e}")
            return None
        except Exception as e:
            print(f"Forecast Processing Error: {e}")
            return None
    
    def get_multiple_cities_weather(self, cities: List[str], units: str = 'metric') -> Dict[str, Dict]:
        """
        Get current weather for multiple cities
        
        Args:
            cities (List[str]): List of city names
            units (str): Units for temperature
            
        Returns:
            Dict: Dictionary with city names as keys and weather data as values
        """
        weather_data = {}
        
        for city in cities:
            data = self.get_current_weather(city, units)
            if data:
                weather_data[city] = data
            else:
                weather_data[city] = None
        
        return weather_data
    
    def get_weather_icon_url(self, icon_code: str) -> str:
        """
        Get the URL for a weather icon
        
        Args:
            icon_code (str): Icon code from API response
            
        Returns:
            str: URL to the weather icon
        """
        return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    
    def is_daytime(self, current_time: datetime, sunrise: datetime, sunset: datetime) -> bool:
        """
        Check if it's currently daytime
        
        Args:
            current_time (datetime): Current time
            sunrise (datetime): Sunrise time
            sunset (datetime): Sunset time
            
        Returns:
            bool: True if daytime, False if nighttime
        """
        return sunrise <= current_time <= sunset
    
    def get_weather_background(self, weather_condition: str, is_day: bool = True) -> str:
        """
        Get appropriate background image based on weather condition
        
        Args:
            weather_condition (str): Weather condition from API
            is_day (bool): Whether it's daytime
            
        Returns:
            str: Background image filename
        """
        weather_backgrounds = {
            'Clear': 'sunny_bg.jpg' if is_day else 'night_bg.jpg',
            'Clouds': 'cloudy_bg.jpg',
            'Rain': 'rainy_bg.jpg',
            'Drizzle': 'rainy_bg.jpg',
            'Thunderstorm': 'stormy_bg.jpg',
            'Snow': 'snowy_bg.jpg',
            'Mist': 'foggy_bg.jpg',
            'Fog': 'foggy_bg.jpg',
            'Haze': 'foggy_bg.jpg'
        }
        
        return weather_backgrounds.get(weather_condition, 'cloudy_bg.jpg')

class WeatherDataProcessor:
    """
    A class to process and analyze weather data
    """
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit"""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius"""
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def get_weather_emoji(weather_condition: str) -> str:
        """Get emoji representation of weather condition"""
        weather_emojis = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Drizzle': '🌦️',
            'Thunderstorm': '⛈️',
            'Snow': '❄️',
            'Mist': '🌫️',
            'Fog': '🌫️',
            'Haze': '🌫️'
        }
        return weather_emojis.get(weather_condition, '🌤️')
    
    @staticmethod
    def get_comfort_level(temperature: float, humidity: float, units: str = 'metric') -> str:
        """
        Get comfort level description based on temperature and humidity
        
        Args:
            temperature (float): Temperature value
            humidity (float): Humidity percentage
            units (str): Temperature units
            
        Returns:
            str: Comfort level description
        """
        # Convert to Celsius if needed
        if units == 'imperial':
            temp_c = WeatherDataProcessor.fahrenheit_to_celsius(temperature)
        else:
            temp_c = temperature
        
        # Basic comfort assessment
        if temp_c < 10:
            return "Cold"
        elif temp_c < 20:
            return "Cool"
        elif temp_c < 25:
            return "Comfortable"
        elif temp_c < 30:
            return "Warm"
        else:
            return "Hot"
    
    @staticmethod
    def format_weather_summary(weather_data: Dict) -> str:
        """
        Format weather data into a readable summary
        
        Args:
            weather_data (Dict): Weather data dictionary
            
        Returns:
            str: Formatted weather summary
        """
        if not weather_data:
            return "No weather data available"
        
        summary = f"""
{weather_data['city']}, {weather_data['country']}
Temperature: {weather_data['temperature']:.1f}°C
Feels like: {weather_data['feels_like']:.1f}°C
Condition: {weather_data['weather_description'].title()}
Humidity: {weather_data['humidity']}%
Wind: {weather_data['wind_speed']} m/s
        """.strip()
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    # Test the WeatherAPI class
    try:
        weather_api = WeatherAPI()
        
        # Test getting current weather
        print("Testing current weather...")
        current_weather = weather_api.get_current_weather("New York")
        if current_weather:
            print("✓ Current weather data retrieved successfully")
            print(WeatherDataProcessor.format_weather_summary(current_weather))
        else:
            print("✗ Failed to retrieve current weather")
        
        # Test forecast
        print("\nTesting forecast...")
        forecast = weather_api.get_forecast("New York", days=3)
        if forecast:
            print(f"✓ Forecast data retrieved: {len(forecast)} data points")
        else:
            print("✗ Failed to retrieve forecast")
            
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Error: {e}")