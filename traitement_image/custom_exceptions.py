COLUMN_IS_MISSING = " column is missing"

class MissingColumnException(Exception):
    
    def __init__(self, column_name):
        self.message = column_name + COLUMN_IS_MISSING
        super().__init__(self.message)