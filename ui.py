import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkinter
import os
from PIL import Image, ImageTk

class WeatherUI:
    """Handle all UI components and layouts"""
    
    def __init__(self, root, app):
        self.root = root
        self.app = app  # Reference to main app
        
        # UI components references
        self.main_frame = None
        self.weather_frame = None
        self.journal_frame = None
        self.forecast_frame = None
        
        # Weather display widgets
        self.location_label = None
        self.temp_label = None
        self.desc_label = None
        self.humidity_label = None
        self.wind_label = None
        self.weather_icon = None
        
        # Search widgets
        self.city_var = tk.StringVar(value="New York")
        self.city_entry = None
        
        # Journal widgets
        self.mood_var = tk.StringVar()
        self.journal_text = None
        
        # Forecast widgets
        self.forecast_fig = None
        self.forecast_ax = None
        self.forecast_canvas = None
        
        # Theme variables
        self.current_theme = 'light'
        
        # Background image
        self.bg_image = None
        self.bg_label = None
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        
        # Setup individual sections
        self.setup_header()
        self.setup_search_section()
        self.setup_weather_section()
        self.setup_journal_section()
        self.setup_forecast_section()
        
        # Try to load background image
        self.load_background_image()
    
    def setup_header(self):
        """Setup application header"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="🌤️ Interactive Weather App", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, 
                                  text="TechPathways Capstone Project - Justice Through Code",
                                  font=("Arial", 10, "italic"))
        subtitle_label.grid(row=1, column=0)
    
    def setup_search_section(self):
        """Setup city search section"""
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # City search
        ttk.Label(search_frame, text="City:").grid(row=0, column=0, padx=(0, 5))
        
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var, width=25)
        self.city_entry.grid(row=0, column=1, padx=(0, 10))
        self.city_entry.bind('<Return>', lambda e: self.app.on_city_search(self.city_var.get()))
        
        # Search button
        search_btn = ttk.Button(search_frame, text="Get Weather", 
                               command=lambda: self.app.on_city_search(self.city_var.get()))
        search_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Theme toggle button
        theme_btn = ttk.Button(search_frame, text="Toggle Dark Mode", 
                              command=self.app.toggle_dark_mode)
        theme_btn.grid(row=0, column=3, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(search_frame, text="🔄 Refresh", 
                                command=lambda: self.app.on_city_search(self.city_var.get()))
        refresh_btn.grid(row=0, column=4)
    
    def setup_weather_section(self):
        """Setup current weather display section"""
        self.weather_frame = ttk.LabelFrame(self.main_frame, text="Current Weather", padding="15")
        self.weather_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configure grid weights
        self.weather_frame.columnconfigure(0, weight=1)
        self.weather_frame.rowconfigure(5, weight=1)
        
        # Weather info labels
        self.location_label = ttk.Label(self.weather_frame, text="Location: --", 
                                       font=("Arial", 12, "bold"))
        self.location_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.temp_label = ttk.Label(self.weather_frame, text="Temperature: --", 
                                   font=("Arial", 16, "bold"))
        self.temp_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.desc_label = ttk.Label(self.weather_frame, text="Description: --", 
                                   font=("Arial", 12))
        self.desc_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.humidity_label = ttk.Label(self.weather_frame, text="Humidity: --", 
                                       font=("Arial", 10))
        self.humidity_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.wind_label = ttk.Label(self.weather_frame, text="Wind: --", 
                                   font=("Arial", 10))
        self.wind_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        # Weather icon area
        icon_frame = ttk.Frame(self.weather_frame)
        icon_frame.grid(row=0, column=1, rowspan=5, padx=(20, 0), sticky=(tk.N, tk.S))
        
        self.weather_icon = ttk.Label(icon_frame, text="🌤️", font=("Arial", 64))
        self.weather_icon.grid(row=0, column=0, pady=20)
        
        # Additional weather info
        info_frame = ttk.Frame(self.weather_frame)
        info_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        
        self.pressure_label = ttk.Label(info_frame, text="Pressure: --", font=("Arial", 10))
        self.pressure_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.visibility_label = ttk.Label(info_frame, text="Visibility: --", font=("Arial", 10))
        self.visibility_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.sunrise_label = ttk.Label(info_frame, text="Sunrise: --", font=("Arial", 10))
        self.sunrise_label.grid(row=0, column=1, sticky=tk.W, padx=(20, 0), pady=2)
        
        self.sunset_label = ttk.Label(info_frame, text="Sunset: --", font=("Arial", 10))
        self.sunset_label.grid(row=1, column=1, sticky=tk.W, padx=(20, 0), pady=2)
    
    def setup_journal_section(self):
        """Setup weather journal section"""
        self.journal_frame = ttk.LabelFrame(self.main_frame, text="Weather Journal", padding="15")
        self.journal_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Configure grid weights
        self.journal_frame.columnconfigure(0, weight=1)
        self.journal_frame.rowconfigure(3, weight=1)
        
        # Mood selection
        ttk.Label(self.journal_frame, text="How's the weather making you feel?").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        mood_combo = ttk.Combobox(self.journal_frame, textvariable=self.mood_var, 
                                 values=self.app.config.get_mood_options(), 
                                 state="readonly")
        mood_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Notes section
        ttk.Label(self.journal_frame, text="Notes:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        # Text area with scrollbar
        text_frame = ttk.Frame(self.journal_frame)
        text_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.journal_text = tk.Text(text_frame, height=8, width=30, wrap=tk.WORD)
        self.journal_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        journal_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.journal_text.yview)
        journal_scrollbar.