from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

#import mysql.connector
def sqlConnect():
    try:
        print('DB connect...')
        mydb = mysql.connector.connect(
            host='10.144.10.75',
            user="btsdba",
            password="masterkey",
            port="3306",
            database="dbmarking"
            )
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM DM')
        result = cursor.fetchall()
        print(result)
        print('Sql ok')
        
    except :
        print('Sql errr')
#sqlConnect()

import pyodbc
cnxn = pyodbc.connect("DRIVER={MySQL ODBC 9.2 Unicode Driver}; SERVER=10.144.10.75;DATABASE=dbmarking; UID=btsdba; PASSWORD=masterkey;")
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM DM")
rows = cursor.fetchall()
for row in rows:
    print(row)
