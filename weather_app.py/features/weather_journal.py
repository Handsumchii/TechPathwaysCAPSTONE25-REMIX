import os
import json
from datetime import datetime
import csv

class WeatherJournal:
    """Handle weather journal functionality"""
    
    def __init__(self, journal_file):
        self.journal_file = journal_file
        self.ensure_journal_file()
    
    def ensure_journal_file(self):
        """Create journal file if it doesn't exist"""
        if not os.path.exists(self.journal_file):
            # Create empty file
            with open(self.journal_file, 'w', encoding='utf-8') as f:
                f.write("=== Weather Journal ===\n")
                f.write("Created on: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                f.write("="*50 + "\n\n")
    
    def save_entry(self, entry_data):
        """Save a journal entry"""
        try:
            # Format the entry
            entry_text = self.format_entry(entry_data)
            
            # Append to file
            with open(self.journal_file, 'a', encoding='utf-8') as f:
                f.write(entry_text)
            
            # Also save to CSV for data analysis
            self.save_to_csv(entry_data)
            
            return True
            
        except Exception as e:
            print(f"Error saving journal entry: {e}")
            return False
    
    def format_entry(self, entry_data):
        """Format entry data into readable text"""
        entry_text = f"""
=== Weather Journal Entry ===
Date: {entry_data['timestamp']}
Location: {entry_data['city']}
Weather: {entry_data['temp']}°C, {entry_data['description']}
Mood: {entry_data['mood']}
Notes: {entry_data['notes']}
{"="*50}

"""
        return entry_text
    
    def save_to_csv(self, entry_data):
        """Save entry to CSV file for data analysis"""
        csv_file = self.journal_file.replace('.txt', '.csv')
        
        # Check if CSV file exists
        file_exists = os.path.exists(csv_file)
        
        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'city', 'temp', 'description', 'mood', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header if file is new
                if not file_exists:
                    writer.writeheader()
                
                # Write entry data
                writer.writerow(entry_data)
                
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def get_recent_entries(self, limit=10):
        """Get recent journal entries"""
        try:
            with open(self.journal_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by entry separator
            entries = content.split("=== Weather Journal Entry ===")
            
            # Return recent entries (excluding header)
            recent_entries = entries[1:limit+1] if len(entries) > 1 else []
            return recent_entries
            
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error reading journal entries: {e}")
            return []
    
    def get_mood_statistics(self):
        """Get statistics about mood entries"""
        csv_file = self.journal_file.replace('.txt', '.csv')
        
        if not os.path.exists(csv_file):
            return {}
        
        try:
            mood_counts = {}
            
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    mood = row['mood']
                    if mood:
                        mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            return mood_counts
            
        except Exception as e:
            print(f"Error getting mood statistics: {e}")
            return {}
    
    def get_weather_mood_correlation(self):
        """Analyze correlation between weather and mood"""
        csv_file = self.journal_file.replace('.txt', '.csv')
        
        if not os.path.exists(csv_file):
            return {}
        
        try:
            weather_moods = {}
            
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    weather_desc = row['description'].lower()
                    mood = row['mood']
                    
                    if weather_desc not in weather_moods:
                        weather_moods[weather_desc] = {}
                    
                    if mood:
                        weather_moods[weather_desc][mood] = weather_moods[weather_desc].get(mood, 0) + 1
            
            return weather_moods
            
        except Exception as e:
            print(f"Error analyzing weather-mood correlation: {e}")
            return {}
    
    def search_entries(self, query):
        """Search journal entries for specific terms"""
        try:
            with open(self.journal_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by entry separator
            entries = content.split("=== Weather Journal Entry ===")
            
            # Search for query in entries
            matching_entries = []
            for entry in entries[1:]:  # Skip header
                if query.lower() in entry.lower():
                    matching_entries.append(entry)
            
            return matching_entries
            
        except Exception as e:
            print(f"Error searching entries: {e}")
            return []
    
    def export_journal(self, export_format='txt'):
        """Export journal in different formats"""
        if export_format == 'txt':
            return self.journal_file
        elif export_format == 'csv':
            return self.journal_file.replace('.txt', '.csv')
        elif export_format == 'json':
            return self.export_to_json()
        else:
            return None
    
    def export_to_json(self):
        """Export journal entries to JSON format"""
        csv_file = self.journal_file.replace('.txt', '.csv')
        json_file = self.journal_file.replace('.txt', '.json')
        
        if not os.path.exists(csv_file):
            return None
        
        try:
            entries = []
            
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    entries.append(dict(row))
            
            with open(json_file, 'w', encoding='utf-8') as jsonfile:
                json.dump(entries, jsonfile, indent=2, ensure_ascii=False)
            
            return json_file
            
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return None
    
    def get_entry_count(self):
        """Get total number of journal entries"""
        csv_file = self.journal_file.replace('.txt', '.csv')
        
        if not os.path.exists(csv_file):
            return 0
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return sum(1 for row in reader)
                
        except Exception as e:
            print(f"Error counting entries: {e}")
            return 0
    
    def get_date_range(self):
        """Get date range of journal entries"""
        csv_file = self.journal_file.replace('.txt', '.csv')
        
        if not os.path.exists(csv_file):
            return None, None
        
        try:
            dates = []
            
            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    dates.append(datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S"))
            
            if dates:
                return min(dates), max(dates)
            else:
                return None, None
                
        except Exception as e:
            print(f"Error getting date range: {e}")
            return None, None
    
    def delete_entry(self, entry_index):
        """Delete a specific journal entry (for cleanup)"""
        # This would be complex to implement with the current file structure
        # For now, just log the request
        print(f"Delete entry request for index: {entry_index}")
        print("Note: Entry deletion not implemented in current version")
        return False
    
    def backup_journal(self):
        """Create a backup of the journal"""
        try:
            backup_file = self.journal_file.replace('.txt', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
            
            with open(self.journal_file, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as backup:
                    backup.write(source.read())
            
            return backup_file
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def get_journal_summary(self):
        """Get a summary of the journal"""
        entry_count = self.get_entry_count()
        date_start, date_end = self.get_date_range()
        mood_stats = self.get_mood_statistics()
        
        summary = {
            'total_entries': entry_count,
            'date_range': {
                'start': date_start.strftime("%Y-%m-%d") if date_start else None,
                'end': date_end.strftime("%Y-%m-%d") if date_end else None
            },
            'mood_statistics': mood_stats,
            'most_common_mood': max(mood_stats.items(), key=lambda x: x[1])[0] if mood_stats else None
        }
        
        return summary