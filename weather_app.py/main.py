import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import threading
from dotenv import load_dotenv

# Import our custom modules
from weather import WeatherAPI
from ui import WeatherUI
from features.weather_journal import WeatherJournal
from features.animated_icons import AnimatedIcons
from features.forecast_comparison import ForecastComparison
from config import Config

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Weather App - TechPathways Capstone")
        self.root.geometry("1000x700")
        
        # Initialize configuration
        self.config = Config()
        
        # Initialize components
        self.weather_api = WeatherAPI(self.config.api_key)
        self.ui = WeatherUI(self.root, self)
        self.journal = WeatherJournal(self.config.journal_file)
        self.animated_icons = AnimatedIcons(self.ui.weather_icon)
        self.forecast = ForecastComparison(self.ui.forecast_canvas, self.ui.forecast_ax, self.ui.forecast_fig)
        
        # Application state
        self.current_weather = None
        self.dark_mode = False
        
        # Initialize UI
        self.ui.setup_ui()
        
        # Load default city
        self.get_weather("New York")
    
    def get_weather(self, city):
        """Main method to get weather data and update all components"""
        try:
            # Get current weather
            self.current_weather = self.weather_api.get_current_weather(city)
            
            if self.current_weather:
                # Update UI with current weather
                self.ui.update_weather_display(self.current_weather)
                
                # Start weather animations
                weather_main = self.current_weather['weather'][0]['main'].lower()
                self.animated_icons.start_animation(weather_main)
                
                # Get and display forecast
                forecast_data = self.weather_api.get_forecast(city)
                if forecast_data:
                    self.forecast.update_forecast(forecast_data)
                    
            else:
                messagebox.showerror("Error", f"Could not fetch weather data for {city}")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def save_journal_entry(self, mood, notes):
        """Save journal entry with current weather data"""
        if not self.current_weather:
            messagebox.showwarning("Warning", "Please get weather data first!")
            return False
        
        if not mood and not notes:
            messagebox.showwarning("Warning", "Please add a mood or some notes!")
            return False
        
        # Prepare entry data
        entry_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'city': self.current_weather['name'],
            'temp': self.current_weather['main']['temp'],
            'description': self.current_weather['weather'][0]['description'],
            'mood': mood,
            'notes': notes
        }
        
        # Save through journal component
        success = self.journal.save_entry(entry_data)
        
        if success:
            messagebox.showinfo("Success", "Journal entry saved!")
            return True
        else:
            messagebox.showerror("Error", "Could not save journal entry")
            return False
    
    def toggle_dark_mode(self):
        """Toggle application theme"""
        self.dark_mode = not self.dark_mode
        self.ui.apply_theme(self.dark_mode)
        
        # Update forecast chart theme
        self.forecast.update_theme(self.dark_mode)
    
    def get_current_weather_data(self):
        """Return current weather data for other components"""
        return self.current_weather
    
    def on_city_search(self, city):
        """Handle city search from UI"""
        if city.strip():
            self.get_weather(city.strip())
    
    def cleanup(self):
        """Clean up resources before closing"""
        # Stop animations
        self.animated_icons.stop_animation()
        
        # Any other cleanup tasks
        print("Application cleanup completed")

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = WeatherApp(root)
    
    # Handle app closing
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        app.cleanup()
    except Exception as e:
        print(f"Application error: {e}")
        app.cleanup()

if __name__ == "__main__":
    main()