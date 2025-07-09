import os
from dotenv import load_dotenv

class Config:
    """Configuration class to manage all app settings"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY not found in environment variables")
        
        # API URLs
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        
        # File paths
        self.data_dir = "data"
        self.journal_file = os.path.join(self.data_dir, "weather_history.txt")
        self.visual_assets_dir = "visual_assets"
        self.background_dir = os.path.join(self.visual_assets_dir, "background")
        self.icons_dir = os.path.join(self.visual_assets_dir, "icons")
        
        # App settings
        self.default_city = "New York"
        self.units = "metric"  # metric, imperial, standard
        self.animation_speed = 1.0  # seconds between animation frames
        
        # UI Settings
        self.window_width = 1000
        self.window_height = 700
        self.padding = 10
        
        # Theme colors
        self.light_theme = {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'accent': '#0078d4',
            'secondary': '#ffffff',
            'text': '#333333'
        }
        
        self.dark_theme = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'accent': '#0078d4',
            'secondary': '#3c3c3c',
            'text': '#ffffff'
        }
        
        # Journal settings
        self.max_journal_entries = 100
        
        # Forecast settings
        self.forecast_days = 5
        
        # Ensure required directories exist
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.data_dir,
            self.visual_assets_dir,
            self.background_dir,
            self.icons_dir
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
    
    def get_background_path(self, weather_condition):
        """Get background image path for weather condition"""
        background_files = {
            'clear': 'clear.jpeg',
            'sunny': 'sunny.jpeg',
            'cloudy': 'cloudy.jpeg',
            'rainy': 'rainy.jpeg',
            'snowy': 'snowy.jpeg',
            'stormy': 'storm.jpeg',
            'home': 'home.jpeg'
        }
        
        filename = background_files.get(weather_condition.lower(), 'home.jpeg')
        return os.path.join(self.background_dir, filename)
    
    def validate_api_key(self):
        """Validate that API key is properly configured"""
        if not self.api_key or self.api_key == 'demo_key':
            return False
        return True
    
    def get_mood_options(self):
        """Get available mood options for journal"""
        return [
            "😊 Happy",
            "😢 Sad", 
            "😴 Sleepy",
            "⚡ Energetic",
            "😌 Peaceful",
            "🤔 Thoughtful",
            "😍 Excited",
            "😤 Frustrated",
            "🥰 Content",
            "😱 Anxious"
        ]
    
    def get_weather_icons(self):
        """Get weather condition to emoji mapping"""
        return {
            'clear': '☀️',
            'clouds': '☁️',
            'rain': '🌧️',
            'drizzle': '🌦️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '🌫️',
            'haze': '🌫️',
            'smoke': '🌫️',
            'dust': '🌪️',
            'sand': '🌪️',
            'ash': '🌋',
            'squall': '💨',
            'tornado': '🌪️'
        }
    
    def get_animation_frames(self):
        """Get animation frames for different weather conditions"""
        return {
            'rain': ['🌧️', '💧', '🌦️', '💧'],
            'clear': ['☀️', '🌞', '☀️', '🌟'],
            'clouds': ['☁️', '⛅', '☁️', '🌤️'],
            'snow': ['❄️', '🌨️', '❄️', '⛄'],
            'thunderstorm': ['⛈️', '🌩️', '⚡', '⛈️'],
            'mist': ['🌫️', '🌁', '🌫️', '🌁'],
            'drizzle': ['🌦️', '🌧️', '🌦️', '💧']
        }
    
    @property
    def app_info(self):
        """Get application information"""
        return {
            'name': 'Interactive Weather App',
            'version': '1.0.0',
            'author': 'Devin Cambridge',
            'description': 'TechPathways Capstone Project - Justice Through Code',
            'github': 'https://github.com/Handsumchii',
            'email': 'Dcambridge7188@gmail.com'
        }