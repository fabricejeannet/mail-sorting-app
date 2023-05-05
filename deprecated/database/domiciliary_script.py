from database_domiciliary_manager import DomiciliaryManager
import sys


domiciliary_manager = DomiciliaryManager()


domiciliary_manager.database_manager.connect_to_database()
args = sys.argv[1:]
if (len(args) < 1 or args[0] == '-h'):

    print("Usage: python3 domiciliary_script.py [option] [domiciliary_name] [domiciliary_key]")

    print("Options: -add, -remove, -get, -get_all, -h")

    print("Example: python3 domiciliary_script.py -add Société 1 123456")

else :
    if (args[0] == "-add"):

        domiciliary_name = args[1]
        if len(args) < 3:
            domiciliary_key = ""
        else : domiciliary_key = args[2]
        domiciliary_manager.add_domiciliary(domiciliary_name, domiciliary_key)

    elif (args[0] == "-remove"):
        domiciliary_name = args[1]
        if len(args) < 3:
            domiciliary_key = ""
        else : domiciliary_key = args[2]
        domiciliary_manager.remove_domiciliary(domiciliary_name)

    elif (args[0] == "-get"):
        print(domiciliary_manager.get_domiciliary(domiciliary_name))

    elif (args[0] == "-get_all"):
        print(domiciliary_manager.get_all_domiciliaries())
    