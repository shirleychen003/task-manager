from models.preferences_model import Preferences

class PreferencesController:
    def __init__(self):
        self.preferences = Preferences()
    
    def apply_theme(self, theme):
        self.preferences.theme = theme
        self.preferences.save_preferences()
    
    def change_font_size(self, size):
        self.preferences.font_size = size
        self.preferences.save_preferences()
    
    def update_color_scheme(self, scheme):
        self.preferences.color_scheme = scheme
        self.preferences.save_preferences()
    
    def load_preferences(self):
        self.preferences.load_preferences() 