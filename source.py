import sqlite3

def main():
    pass


class UI:
    pass



class Database:
    def __init__(self):
        self.db_path = ""
        self.connection = sqlite2.connect(db_path)
        self.cursor = connection.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.connection.close()
        
        
main()