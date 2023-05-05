from database_alias_manager import AliasManager
import sys

alias_manager = AliasManager()

alias_manager.database_manager.connect_to_database()

args = sys.argv[1:]

if (len(args) < 1 or args[0] == '-h'):
    print("Usage: python3 alias_script.py [option] [alias_text] [company_id]/[company_name]")
    print("Options: -add_id, -add_name, -remove, -get_all, -h")
    print("Example: python3 alias_script.py -add_name coulworking CoolWorking")
else:
    if (args[0] == "-add_id"):
        alias_text = args[1]
        company_name = args[2]
        alias_manager.add_alias_with_company_id(alias_text, company_id)
    elif (args[0] == "-add_name"):
        alias_text = args[1]
        company_name = args[2]
        alias_manager.add_alias_with_company_name(alias_text, company_name)
    elif (args[0] == "-remove"):
        alias_text = args[1]
        alias_manager.remove_alias(alias_text)
    elif (args[0] == "-get_all"):
        print(alias_manager.get_all_company_alias(company_name=args[1]))