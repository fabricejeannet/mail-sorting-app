import pandas

import pytest

import database.csv_constants as csv_constants


class CsvManager :
    

    def __init__(self):
        self.dataframe = pandas.DataFrame()


    def check_file_type(self,file_name) :
        
        return file_name.lower().endswith(".csv")


    def open_csv(self,file_name) :
        
        self.dataframe = pandas.read_csv(file_name)
        

    def close_csv(self) :

        self.dataframe = pandas.DataFrame()


    def get_company_names(self) :

        return self.dataframe[csv_constants.RAISON_SOCIALE]
    

    def get_legal_representatives(self) :

        return self.dataframe[csv_constants.REPRESENTANT_LEGAL]

    def get_subscription_status(self) :

        return self.dataframe[csv_constants.STATUT]
    

    def get_director_names(self) :

        return self.dataframe[csv_constants.NOM_PRENOM_DIRIGEANT]
    

    def get_row_from_index(self, index) :

        return self.dataframe.iloc[index]
    

    def get_company_name_from_index(self, index) :

        return self.get_row_from_index(index)[csv_constants.RAISON_SOCIALE]
    

    def get_legal_representative_from_index(self, index) :

        return self.get_row_from_index(index)[csv_constants.REPRESENTANT_LEGAL]
    
    def get_external_id_from_index(self, index) :

        return self.get_row_from_index(index)[csv_constants.IDENTIFIANT]

    def get_subscription_status_from_index(self, index) :

        return self.get_row_from_index(index)[csv_constants.STATUT]
    

    def get_director_name_from_index(self, index) :

        if pandas.isnull(self.get_row_from_index(index)[csv_constants.NOM_PRENOM_DIRIGEANT]) :
            return ""

        return self.get_row_from_index(index)[csv_constants.NOM_PRENOM_DIRIGEANT]

    def get_only_director_first_name_from_index(self, index) :

        director_name = self.get_director_name_from_index(index)

        if director_name == "" :
            return ""

        return director_name.split(" ")[0]
    

    def get_only_director_last_name_from_index(self, index) :

        director_name = self.get_director_name_from_index(index)

        if director_name == "" :
            return ""

        return director_name.split(" ")[1]
    
    

    

    # def create_test_csv(self):

    #     with open("test.csv", "w") as test_file:

    #         test_file.write("Dénomination sociale,Représentant légal,Statut Abonnement,nom prenom date de naissance du dirigeant\n")

    #         test_file.write("Société 1,Mr. Grutier,ABONNE,Jean Grutier\n")

    #         test_file.write("Société 2,Mr. Laurent,ABONNE,Louis Laurent\n")

    #         test_file.write("Société 3,Mr. Dupont,ABONNE,Paul Dupont\n")

    #         test_file.write("Société 4,Mr. Durand,DESABONNE,Paul Durand\n")

    #         test_file.write("Société 5,Mme. Martin,DESABONNE,Paule Martin\n")

    #         test_file.write("Société 6,Mme. Bernard,RADIE,Paule Bernard\n")
    