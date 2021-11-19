from flask import Flask,render_template,redirect,request,session
from datetime import datetime
from Sql_Querries import CheckUser,CheckMail,CheckLogin,InsertUser
app=Flask(__name__)
app.secret_key = "cn assignment safty key **&**"

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/Login',methods=['POST','GET'])
def Login():
    ques=[[1,1,'This is a good QUESTION',0,'22-3-2021'],[2,1,'nOT SO OMPRESSEIVE',0,'22-6-2021'],[3,2,'My good ness',1,'22-12021']]
    if request.method=="POST":
        Uname=request.form['Uname']
        Password=request.form['Password']
        if(CheckLogin(Uname,Password)):
            session['username']=Uname
        else:
            print("Wrong Username and password")
            return redirect('/')
    return render_template('Home.html',Questions=ques)

@app.route('/Signup',methods=['POST','GET'])
def Signup():
    if(request.method=="POST"):
        Uname=request.form['Uname']
        Password=request.form['Password']
        Email=request.form['Email']
        if(CheckUser(Uname)):
            print("User already present")
        elif(CheckMail(Email)):
            print("Mail already taken")
        else:
            InsertUser(Uname,Email,Password)        
    return render_template('Login.html')    

@app.route('/Home')
def Home():
    if(not session.get('username',None)):
        return render_template('Login.html')
    else:
        return render_template('Home.html')

@app.route('/Logout')
def Logout():
    session.pop('username',None)
    return render_template('Login.html')

@app.route('/Profile')
def Profile():
    return render_template('Profile.html')


if __name__=="__main__":
    app.run(debug=True)