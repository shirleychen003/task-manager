import json
import os

class Preferences:
    def __init__(self, theme='Light', font_size=12, color_scheme='Default'):
        self.theme = theme
        self.font_size = font_size
        self.color_scheme = color_scheme

    def save_preferences(self, file_path='utils/preferences.json'):
        preferences = {
            'theme': self.theme,
            'font_size': self.font_size,
            'color_scheme': self.color_scheme
        }
        with open(file_path, 'w') as f:
            json.dump(preferences, f)

    def load_preferences(self, file_path='utils/preferences.json'):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                preferences = json.load(f)
                self.theme = preferences.get('theme', 'Light')
                self.font_size = preferences.get('font_size', 12)
                self.color_scheme = preferences.get('color_scheme', 'Default') 