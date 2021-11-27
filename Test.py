import sqlite3
conn=sqlite3.connect('quora.db')
cur=conn.cursor()
# cur.execute('''Select name from sqlite_master where type='table';''')
cur.execute('''Select * from Votes;''')
print(cur.fetchall())

# import datetime
# nw=str(datetime.datetime.now())
# nw=datetime.datetime.fromisoformat(nw)
# print(nw,type(nw))