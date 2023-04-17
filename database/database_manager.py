import mysql.connector

class DatabaseManager:
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect_to_database(self) :
        try:
            self.connection = mysql.connector.connect(
                                                host='localhost',
                                                user='root',
                                                password='plop',
                                                database='clients_test'
                                            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        
    
    def execute_void_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def execute_fetchall_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_fetchone_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()
    
    def empty_society_table(self):
        self.execute_void_query("TRUNCATE TABLE societes")
        
    def empty_domiciliary_table(self):
        self.execute_void_query("TRUNCATE TABLE domiciliataires")
    
    def empty_alias_table(self):
        self.execute_void_query("TRUNCATE TABLE alias")
    
    def empty_all_tables(self):
        self.empty_society_table()
        self.empty_domiciliary_table()
        self.empty_alias_table()
    
    def disconnect_from_database(self):
        if self.connection != None and self.connection.is_connected():
            self.connection.close()
            self.cursor.close()
            print("MySQL connection is closed")
        else :
            print("MySQL connection is not open")