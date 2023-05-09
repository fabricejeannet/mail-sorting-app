COLUMN_IS_MISSING = " column is missing"

class MissingColumnException(Exception):
    
    def __init__(self, column_name):
        self.message = column_name + COLUMN_IS_MISSING
        super().__init__(self.message)
        

class NoTextFoundOnPicture(Exception):
    def __init__(self):
        self.message = "No text found in the image"   
        
        
class TryToOpenNonCsvFile(Exception):
    def __init__(self):
        self.message = "Try to open a non csv file"
        
        
class TryToOpenEmptyCsvFile(Exception):
    def __init__(self):
        self.message = "Try to open an empty csv file"
        
        
class NoImageGiven(Exception):
    def __init__(self):
        self.message = "No image given"