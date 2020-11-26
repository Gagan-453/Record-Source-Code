import sqlite3 as sq
conn = sq.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM YOUR_FILES WHERE FILE = "g"')
print(cursor.fetchall())
conn.close()

# SELECT * FROM YOUR_FILES
# CREATE TABLE YOUR_FILES(FILE LONGTEXT, PASSWORD, DATE, CONTENT)
# DROP TABLE YOUR_FILES