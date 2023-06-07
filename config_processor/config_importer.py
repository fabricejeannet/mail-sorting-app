import json
from config_processor.config_constants import *
from csv_processor.csv_constants import *

class ConfigImporter:
    
    def __init__(self):
        self.config_file_path = JSON_FILE_PATH
        self.config = self.import_config()


    def import_config(self):
        with open(self.config_file_path) as config_file:
            config = json.load(config_file)
            return config
        
    
    def get_csv_file_path(self):
        return self.config["csv"]["filepath"]
    
    
    def get_csv_file_regex(self):
        return self.config["csv"]["regex"]
    
    
    def get_image_valid_threshold(self):
        return self.config["image"]["valid_ratio_threshold"]
    
    
    def get_image_minimum_threshold(self):
        return self.config["image"]["minimum_valid_ratio_threshold"]
    
    
    def get_keyboard_icon_path(self):
        return self.config["icons"]["keyboard_icon_path"]
    
    
    def get_camera_icon_path(self):
        return self.config["icons"]["camera_icon_path"]
    
    
    def get_shaking_camera_icon_path(self):
        return self.config["icons"]["shaking_camera_icon_path"]
    
    
    def get_valid_icon_path(self):
        return self.config["icons"]["valid_icon_path"]
    
    
    def get_invalid_icon_path(self):
        return self.config["icons"]["invalid_icon_path"]
    
    
    def get_warning_icon_path(self):
        return self.config["icons"]["warning_icon_path"]
    
    
    def get_human_icon_path(self):
        return self.config["icons"]["human_icon_path"]
    
    
    def get_company_icon_path(self):
        return self.config["icons"]["company_icon_path"]
    
    
    def get_welcome_message(self):
        return self.config["messages"]["welcome_message"]
    
    
    def get_valid_message(self):
        return self.config["messages"]["valid_message"]
    
    
    def get_invalid_unsubscribed_message(self):
        return self.config["messages"]["invalid_unsubscribed_message"]
    
    
    def get_invalid_not_found_message(self):
        return self.config["messages"]["invalid_not_found_message"]
    
    
    def get_warning_status_message(self):
        return self.config["messages"]["warning_status_message"]
    
    
    def get_warning_ratio_message(self):
        return self.config["messages"]["warning_ratio_message"]
    
    
    def get_movement_detected_message(self):
        return self.config["messages"]["movement_detected_message"]
    
    
    def get_analysing_message(self):
        return self.config["messages"]["analysing_message"]
    
    def get_no_text_found_message(self):
        return self.config["messages"]["no_text_found_message"]
    
    