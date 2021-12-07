import sqlite3

class database():
    databasename = 'data.db'
    tablename = 'stock'
    create_table = '''
       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);'''
    
    def __init__(self):
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        self.c.execute(f"CREATE TABLE IF NOT EXISTS {self.tablename} {self.create_table}")
        self.conn.commit()
        self.conn.close()
    
    def emptytable(self):
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        self.c.execute(f"DROP TABLE {self.tablename};")
        self.c.execute(f"CREATE TABLE IF NOT EXISTS {self.tablename} {self.create_table}")
        self.conn.commit()
        self.conn.close()
    
    def insert(self):
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        self.c.execute(f"INSERT INTO {self.tablename} (NAME,AGE,ADDRESS,SALARY) \
      VALUES ('Paul', 32, 'California', 20000.00 )")
        self.conn.commit()
        self.conn.close()

    # def update(self):
    #     self.conn = sqlite3.connect(self.databasename)
    #     self.c = self.conn.cursor()
    #     self.c.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
    #     self.conn.commit()
    #     self.conn.close()

    def selectall(self):
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        cursor = self.c.execute(f"SELECT * from {self.tablename}")
        self.conn.commit()
        self.conn.close()
        return cursor
    
    def printall(self):
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        cursor = self.c.execute(f"SELECT * from {self.tablename}")
        names = [description[0] for description in cursor.description]
        print(names)
        for row in cursor:
            print(row)
        self.conn.commit()
        self.conn.close()


def main():
    db = database()
    db.insert()
    db.printall()
    db.emptytable()
    db.printall()

if __name__ == "__main__":
    main()