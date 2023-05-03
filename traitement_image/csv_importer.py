import pandas
from custom_exceptions import *
import pytest

import csv_constants as csv_constants


class CsvManager :
    

    def __init__(self):
        self.dataframe = pandas.DataFrame()


    def check_file_type(self,file_name) :
        
        return file_name.lower().endswith(".csv")


    def load_dataframe_from_csv_file(self,file_name) :
        
        self.dataframe = pandas.read_csv(file_name)
        

    def reset_dataframe(self) :

        self.dataframe = pandas.DataFrame()


    def get_ids(self):
        try :
            res = self.dataframe[csv_constants.IDENTIFIANT]
        except :
            raise MissingColumnException("id")
        return res

    def get_company_names(self) :
        try :
            res = self.dataframe[csv_constants.RAISON_SOCIALE]
        except :
            raise MissingColumnException("company")
        return self.dataframe[csv_constants.RAISON_SOCIALE]
    

    def get_legal_representatives(self) :
        return self.dataframe[csv_constants.REPRESENTANT_LEGAL]


    def get_subscription_status(self) :
        return self.dataframe[csv_constants.STATUT]
    

    def get_director_names(self) :
        return self.dataframe[csv_constants.NOM_PRENOM_DIRIGEANT]    


    def get_trademark_names(self) :
        return self.dataframe[csv_constants.MARQUE_COMMERCIALE]