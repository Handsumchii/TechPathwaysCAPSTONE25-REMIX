import threading
import time
import tkinter as tk
from tkinter import ttk

class AnimatedIcons:
    """Handle animated weather icons"""
    
    def __init__(self, icon_widget):
        self.icon_widget = icon_widget
        self.animation_thread = None
        self.animation_running = False
        self.current_weather = None
        self.animation_speed = 1.0  # seconds between frames
        
        # Animation frames for different weather conditions
        self.animation_frames = {
            'rain': ['🌧️', '💧', '🌦️', '💧', '🌧️'],
            'drizzle': ['🌦️', '🌧️', '🌦️', '💧', '🌦️'],
            'clear': ['☀️', '🌞', '☀️', '🌟', '☀️'],
            'sunny': ['☀️', '🌞', '☀️', '🌟', '☀️'],
            'clouds': ['☁️', '⛅', '☁️', '🌤️', '☁️'],
            'partly_cloudy': ['⛅', '🌤️', '⛅', '☁️', '⛅'],
            'snow': ['❄️', '🌨️', '❄️', '⛄', '❄️'],
            'thunderstorm': ['⛈️', '🌩️', '⚡', '⛈️', '🌩️'],
            'mist': ['🌫️', '🌁', '🌫️', '🌁', '🌫️'],
            'fog': ['🌫️', '🌁', '🌫️', '🌁', '🌫️'],
            'haze': ['🌫️', '🌁', '🌫️', '🌁', '🌫️'],
            'smoke': ['🌫️', '💨', '🌫️', '💨', '🌫️'],
            'dust': ['🌪️', '💨', '🌪️', '💨', '🌪️'],
            'sand': ['🌪️', '💨', '🌪️', '💨', '🌪️'],
            'ash': ['🌋', '💨', '🌋', '💨', '🌋'],
            'squall': ['💨', '🌪️', '💨', '🌪️', '💨'],
            'tornado': ['🌪️', '🌪️', '🌪️', '🌪️', '🌪️']
        }
        
        # Special effects for different conditions
        self.special_effects = {
            'thunderstorm': self.thunderstorm_effect,
            'rain': self.rain_effect,
            'snow': self.snow_effect,
            'clear': self.sunny_effect
        }
    
    def start_animation(self, weather_type):
        """Start animation for given weather type"""
        # Stop any existing animation
        self.stop_animation()
        
        self.current_weather = weather_type.lower()
        self.animation_running = True
        
        # Start animation thread
        self.animation_thread = threading.Thread(target=self.animate_weather)
        self.animation_thread.daemon = True
        self.animation_thread.start()
    
    def stop_animation(self):
        """Stop current animation"""
        if self.animation_running:
            self.animation_running = False
            
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1)
    
    def animate_weather(self):
        """Main animation loop"""
        if not self.current_weather:
            return
        
        # Get animation frames for current weather
        frames = self.animation_frames.get(self.current_weather, ['🌤️'])
        frame_index = 0
        
        # Special effects counter
        effect_counter = 0
        
        try:
            while self.animation_running:
                # Update icon
                current_frame = frames[frame_index]
                self.update_icon(current_frame)
                
                # Apply special effects occasionally
                if effect_counter % 10 == 0:  # Every 10 frames
                    self.apply_special_effect()
                
                # Move to next frame
                frame_index = (frame_index + 1) % len(frames)
                effect_counter += 1
                
                # Wait before next frame
                time.sleep(self.animation_speed)
                
        except Exception as e:
            print(f"Animation error: {e}")
        finally:
            self.animation_running = False
    
    def update_icon(self, icon_text):
        """Update icon widget with new text"""
        try:
            if self.icon_widget.winfo_exists():
                # Schedule update on main thread
                self.icon_widget.after(0, lambda: self.icon_widget.config(text=icon_text))
        except tk.TclError:
            # Widget was destroyed
            self.animation_running = False
    
    def apply_special_effect(self):
        """Apply special effects based on weather type"""
        if self.current_weather in self.special_effects:
            try:
                self.special_effects[self.current_weather]()
            except Exception as e:
                print(f"Special effect error: {e}")
    
    def thunderstorm_effect(self):
        """Special effect for thunderstorms"""
        # Flash effect
        original_bg = self.icon_widget.cget('background')
        
        def flash():
            try:
                if self.icon_widget.winfo_exists():
                    self.icon_widget.config(background='yellow')
                    self.icon_widget.after(100, lambda: self.icon_widget.config(background=original_bg))
            except tk.TclError:
                pass
        
        if self.animation_running:
            self.icon_widget.after(0, flash)
    
    def rain_effect(self):
        """Special effect for rain"""
        # Brief size change to simulate rain drops
        original_font = self.icon_widget.cget('font')
        
        def rain_drop():
            try:
                if self.icon_widget.winfo_exists():
                    # Make icon slightly larger
                    current_font = list(original_font)
                    current_font[1] += 5  # Increase size by 5
                    self.icon_widget.config(font=tuple(current_font))
                    
                    # Return to normal size
                    self.icon_widget.after(200, lambda: self.icon_widget.config(font=original_font))
            except (tk.TclError, TypeError):
                pass
        
        if self.animation_running:
            self.icon_widget.after(0, rain_drop)
    
    def snow_effect(self):
        """Special effect for snow"""
        # Gentle floating effect
        original_font = self.icon_widget.cget('font')
        
        def snow_float():
            try:
                if self.icon_widget.winfo_exists():
                    # Slightly reduce size for floating effect
                    current_font = list(original_font)
                    current_font[1] -= 3  # Decrease size by 3
                    self.icon_widget.config(font=tuple(current_font))
                    
                    # Return to normal size
                    self.icon_widget.after(300, lambda: self.icon_widget.config(font=original_font))
            except (tk.TclError, TypeError):
                pass
        
        if self.animation_running:
            self.icon_widget.after(0, snow_float)
    
    def sunny_effect(self):
        """Special effect for sunny weather"""
        # Bright glow effect
        original_fg = self.icon_widget.cget('foreground')
        
        def sun_glow():
            try:
                if self.icon_widget.winfo_exists():
                    self.icon_widget.config(foreground='gold')
                    self.icon_widget.after(150, lambda: self.icon_widget.config(foreground=original_fg))
            except tk.TclError:
                pass
        
        if self.animation_running:
            self.icon_widget.after(0, sun_glow)
    
    def set_animation_speed(self, speed):
        """Set animation speed (seconds between frames)"""
        self.animation_speed = max(0.1, min(5.0, speed))  # Clamp between 0.1 and 5.0
    
    def get_static_icon(self, weather_type):
        """Get static icon for weather type (no animation)"""
        weather_icons = {
            'clear': '☀️',
            'sunny': '☀️',
            'clouds': '☁️',
            'partly_cloudy': '⛅',
            'rain': '🌧️',
            'drizzle': '🌦️',
            'thunderstorm': '⛈️',
            'snow': '❄️',
            'mist': '🌫️',
            'fog': '