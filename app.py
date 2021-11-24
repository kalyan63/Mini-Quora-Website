from flask import Flask,render_template,redirect,request,session
from datetime import datetime
from Sql_Querries import CheckUser,CheckMail,CheckLogin,InsertUser,DisplayQues,GetUserId,InsertQues
app=Flask(__name__)
app.secret_key = "cn assignment safty key **&**"

@app.route('/')
def index():
    return render_template('Login.html')

@app.route('/Login',methods=['POST','GET'])
def Login():
    if request.method=="POST":
        Uname=request.form['Uname']
        Password=request.form['Password']
        if(CheckLogin(Uname,Password)):
            session['UserId']=GetUserId(Uname)
        else:
            print("Wrong Username and password")
            return redirect('/')
    return render_template('Home.html',Questions=DisplayQues())

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

@app.route('/Home',methods=["POST"])
def Home():
    if(request.method=="POST"):
        Q_Text=request.form['q_text']
        An=int(request.form.get('anonymous',0))   
        user_id=session['UserId']
        if(Q_Text):
            InsertQues(user_id,Q_Text,An)
        else:
            print("Please enter a question") 
        return render_template('Home.html')    
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