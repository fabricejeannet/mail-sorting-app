from watchdog.events import FileSystemEventHandler
import logging

class CsvHandler(FileSystemEventHandler):  
    
    def __init__(self, controller):
        self.controller = controller   
        logging.info("CsvHandler initialized")
    
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info("New csv file detected: " + event.src_path)
            logging.info("Processing csv file...")
            
            self.controller.init_csv()
                
    
    def on_deleted(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logging.info("Csv file deleted: " + event.src_path)
            logging.info("Processing csv file...")
            self.controller.init_csv()
