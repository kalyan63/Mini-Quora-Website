import sqlite3
import os
import hashlib
from datetime import datetime

def CheckUser(Uname):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Count(*) from User where User_name = ?",(Uname,))
    ct=cur.fetchone()
    conn.close()
    return(ct[0])

def CheckMail(Mail):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Count(*) from User where Email = ?",(Mail,))
    ct=cur.fetchone()
    conn.close()
    return(ct[0])

def InsertUser(Uname,Mail,Password):
    salt=os.urandom(8)
    hash=hashlib.pbkdf2_hmac('sha256', Password.encode('utf-8'), salt, 100000)
    Cur_date=str(datetime.now())
    arg=(Uname,hash,salt,Mail,Cur_date)
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Insert into User(User_name,Password,Salt,Email,LastLogin) values(?,?,?,?,?)",arg)
    conn.commit()
    conn.close()

def CheckLogin(Uname,Password):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select Password,Salt from User where User_name=?",(Uname,))
    res=cur.fetchone()
    conn.close()
    if(not res):
        return 0
    DbPassword,salt=res[0],res[1]
    if(hashlib.pbkdf2_hmac('sha256', Password.encode('utf-8'), salt, 100000)==DbPassword):
        return 1
    else:
        return 0

def GetUserId(Uname):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select user_id from User where User_name=?",(Uname,))
    res=cur.fetchone()
    conn.close()
    return res[0]

def GetUserName(U_Id):
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Select User_name from User where user_id=?",(U_Id,))
    res=cur.fetchone()
    conn.close()
    return res[0]

def DisplayQues(): 
    conn = sqlite3.connect('quora.db') 
    cur = conn.cursor() 
    cur.execute("select * from Questions") 
    data = cur.fetchall()  
    conn.close()
    return(data)

def InsertQues(user_id,Q_Text,An):
    Cur_date=str(datetime.now())
    arg=(user_id,Q_Text,An,Cur_date)
    conn=sqlite3.connect('quora.db')
    cur=conn.cursor()
    cur.execute("Insert into Questions(user_id,Q_Text,Ananymous,Date) values(?,?,?,?)",arg)
    conn.commit()
    conn.close()

def DisplayQuesUser(user_id):
    conn = sqlite3.connect('quora.db') 
    cur = conn.cursor() 
    cur.execute("select * from Questions where user_id=user_id") 
    data = cur.fetchall()  
    conn.close()
    return(data)

def DisplayAnsUser(user_id):
    conn = sqlite3.connect('quora.db') 
    cur = conn.cursor() 
    cur.execute("select * from Answer where user_id=user_id") 
    data = cur.fetchall()  
    conn.close()
    return(data)

def Getemail(user_id):
    conn = sqlite3.connect('quora.db') 
    cur = conn.cursor() 
    cur.execute("select Email from User where user_id=?",(user_id,)) 
    data = cur.fetchall()[0]
    conn.close()
    return(data)
