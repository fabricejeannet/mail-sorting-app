import tkinter as tk
from streetfacteur_processor.app_back import AppBack
from streetfacteur_processor.app_gui import AppGui
from csv_processor.csv_handler import CsvHandler
from watchdog.observers import Observer
import time
import cProfile
from config_processor.config_importer import ConfigImporter


config_importer = ConfigImporter()

app_gui = AppGui()
app_back = AppBack(app_gui)
observer = Observer()
event_handler = CsvHandler(app_back)
observer.schedule(event_handler, path=config_importer.get_csv_file_path(), recursive=False)
observer.start()
app_back.main()
# run the observer infinitely
# try:
#     while True:
#         time.sleep(10)
# except KeyboardInterrupt:
#     observer.stop()