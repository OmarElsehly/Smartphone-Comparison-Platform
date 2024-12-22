import sqlite3

conn = sqlite3.connect('FinalPhonesDataBase.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)
