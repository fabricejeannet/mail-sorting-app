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
        
    
class UnexpectedCsvFile(Exception):
    def __init__(self):
        self.message = "Unexpected csv file"
        
        
class TryToOpenEmptyCsvFile(Exception):
    def __init__(self):
        self.message = "Try to open an empty csv file"
        
        
class NoImageGiven(Exception):
    def __init__(self):
        self.message = "No image given"
        
        
class CameraIsNotStarted(Exception):
    def __init__(self):
        self.message = "Camera is not started, please start it before taking a picture"
        
        
class NoCsvFileFound(Exception):
    def __init__(self):
        self.message = "No csv file found"