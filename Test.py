import sqlite3
conn=sqlite3.connect('quora.db')
cur=conn.cursor()
cur.execute('''Select name from sqlite_master where type='table';''')
print(cur.fetchall())