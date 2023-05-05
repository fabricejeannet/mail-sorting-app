from csv_processor.csv_constants import *


class Client:
    
    def __init__(self, id, company_name, legal_representative, subscription_status, director_name, trademark_name):
        self.id = id
        self.company_name = company_name
        self.legal_representative = legal_representative
        self.subscription_status = subscription_status
        self.director_name = director_name
        self.trademark_name = trademark_name