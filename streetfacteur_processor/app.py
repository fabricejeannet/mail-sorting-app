import tkinter as tk
import street_facteur_gui
from street_facteur_gui import StreetFacteur
from csv_processor.csv_handler import CsvHandler
from watchdog.observers import Observer
import time
from config_processor.config_importer import ConfigImporter


street_facteur_gui = StreetFacteur()
config_importer = ConfigImporter()
observer = Observer()
event_handler = CsvHandler(street_facteur_gui)
observer.schedule(event_handler, path=config_importer.get_csv_file_path(), recursive=False)
observer.start()
street_facteur_gui.main()
# run the observer infinitely
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()