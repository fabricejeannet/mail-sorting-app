import time
from config_processor.config_importer import ConfigImporter
from watchdog.observers import Observer
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
            
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info("Csv file modified: " + event.src_path)
            logging.info("Processing csv file...")
            self.street_facteur.init_csv()
    
    
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info("Csv file deleted: " + event.src_path)
            logging.info("Processing csv file...")
            self.street_facteur.init_csv()

if __name__ == "__main__":
    config_importer = ConfigImporter()
    observer = Observer()
    event_handler = CsvHandler()
    observer.schedule(event_handler, path=config_importer.get_csv_file_path(), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
