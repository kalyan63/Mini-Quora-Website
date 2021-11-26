import sqlite3
conn=sqlite3.connect('quora.db')
cur=conn.cursor()

#There are just Five data types in sqlite3, 
#Text, Integer, Real, Blob
#So all below mentioned data types would be converted to standard data types according to the rules mentioned in the 
# official website. 

table1='''Create Table IF NOT EXISTS User(
    user_id     INTEGER PRIMARY KEY autoincrement,
    User_name   varchar(20),
    Password    blob(50),
    Salt        blob(8),
    Email       varchar(40),
    LastLogin   Text);'''

table2='''Create Table IF NOT EXISTS Follow(
    user_id     int,
    follow_id   int,
    Date        Text);'''

table3='''Create Table IF NOT EXISTS Questions(
    Q_id        INTEGER PRIMARY KEY autoincrement,
    user_id     int not null,
    Q_Text      varchar(500),
    Anonymous   int default 0,
    Date        Text);'''

table4='''Create Table IF NOT EXISTS Answer(
    A_id        INTEGER PRIMARY KEY autoincrement,
    Q_id        int not null,
    user_id     int not null,
    A_Text      varchar(500),
    Upvote_count    int default 0,
    Downvote_count  int default 0,
    Date        Text,
    Anonymous   int default 0);'''

table5='''Create Table IF NOT EXISTS Media(
    M_id        INTEGER PRIMARY KEY autoincrement,
    A_id        int,
    File_loc    varchar(40));'''

table6='''Create Table IF NOT EXISTS Votes(
    V_id        INTEGER PRIMARY KEY autoincrement,
    A_id        int not null,
    user_id     int not null,
    vote_type   int default 1);'''

table7='''Create Table IF NOT EXISTS Comments(
    C_id        INTEGER PRIMARY KEY autoincrement,
    A_id        int not null,
    user_id     int not null,
    Text        varchar(500),
    Anonymous   int default 0);'''

Tables=[table1,table2,table3,table4,table5,table6,table7]
for table in Tables:
    cur.execute(table)
conn.commit()
conn.close()    