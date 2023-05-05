from database_alias_manager import AliasManager
from database_domiciliary_manager import DomiciliaryManager
from database_society_manager import SocietyManager
from alive_progress import alive_bar
from csv_importer import CsvManager
import sys
import time 

society_manager = SocietyManager()
domiciliary_manager = DomiciliaryManager()
csv_manager = society_manager.csv_manager
society_manager.database_manager.connect_to_database()
domiciliary_manager.database_manager.connect_to_database()

args = sys.argv[1:]

if (len(args) < 1 or args[0] == '-h'):
    print("Usage: python3 csv_society_script.py [option] [domiciliary_name] [csv_file_path]")
    print("Options: -h, -add, -remove_all, -remove")
    print("Example: python3 csv_society_script.py -h")
    print("Example: python3 csv_society_script.py -add CoolWorking csv_file.csv")

elif (args[0] == "-add"):
    if (csv_manager.check_file_type(args[2])):
        print("File type is correct")
        csv_manager.open_csv(args[2])
        if (not domiciliary_manager.check_if_domiciliary_already_exist_from_name(args[1])):
            saisie = input("Domiciliary does not exist, do you want to create it ? (y/n) ")
            if saisie == "y":
                saisie = input("Does your domiciliary have an domiciliary key ? (y/n) ")
                if (saisie == "y"):
                    domiciliary_key = input("Please enter the domiciliary key: ")
                    domiciliary_manager.add_domiciliary(args[1], domiciliary_key)
                else :
                    domiciliary_manager.add_domiciliary(args[1], None)
            else:
                raise Exception("Domiciliary does not exist, you need one to create a society")
        domiciliary_id = domiciliary_manager.get_domiciliary_id_from_name(args[1])
        added_lines = 0
        total_lines = len(csv_manager.dataframe)
        with alive_bar(total_lines) as bar:
            for index, row in csv_manager.dataframe.iterrows():
                try:
                    society_manager.add_society(index, domiciliary_id)
                    added_lines += 1
                except Exception as e:
                    print(e)
                bar(added_lines)
                time.sleep(0.01)
    else:
        raise Exception("File type is incorrect")
elif (args[0] == "-remove_all"):
    society_manager.remove_all_societies()
elif (args[0] == "-remove"):
    society_manager.remove_society(args[1])
    