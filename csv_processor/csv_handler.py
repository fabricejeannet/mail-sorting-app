import time
from config_processor.config_importer import ConfigImporter
from watchdog.events import FileSystemEventHandler
import logging

class CsvHandler(FileSystemEventHandler):  
    
    def __init__(self, street_facteur):
        self.street_facteur = street_facteur   
        logging.info("CsvHandler initialized")
    
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info("New csv file detected: " + event.src_path)
            logging.info("Processing csv file...")
            self.street_facteur.init_csv()
                
    
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info("Csv file deleted: " + event.src_path)
            logging.info("Processing csv file...")
            self.street_facteur.init_csv()
