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
    