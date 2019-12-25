import os, sys, pyodbc

import pyodbc

dbName = r'C:\Users\llassetter\Documents\AccessODBC\SilvercityWP347.mdb'
odbc_connect_str = 'Driver={Microsoft Access Driver (*.mdb)};DBQ=%s' % (dbName)

conn = pyodbc.connect(odbc_connect_str)
cursor = conn.cursor()
cursor.execute('select * from 933768')

for row in cursor.fetchall():
    print (row)