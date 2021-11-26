from flask import Flask,render_template,redirect,request,session
from datetime import datetime
from Sql_Querries import CheckUser,CheckMail,CheckLogin, GetFileLoc, InsertFiles,InsertUser,DisplayQues,GetUserId,GetUserMail,InsertQues,GetQuestion,GetAnswer,InsertAns,GetUserName,UpVote_Answer,DownVote,InsertFiles,GetFileLoc
import os
app=Flask(__name__)
app.secret_key = "cn assignment safty key **&**"
app.config['UPLOAD_FOLDER']='ImgFolder/'
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
    return render_template('Home.html',Questions=DisplayQues(),get_Name=GetUserName)

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

@app.route('/Home',methods=["POST","GET"])
def Home():
    if(request.method=="POST"):
        Q_Text=request.form['q_text']
        An=int(request.form.get('anonymous',0))   
        user_id=session['UserId']
        if(Q_Text):
            InsertQues(user_id,Q_Text,An)
        else:
            print("Please enter a question") 
        return render_template('Home.html',Questions=DisplayQues(),get_Name=GetUserName)    
    if(not session.get('UserId',None)):
        return render_template('Login.html')
    else:
        return render_template('Home.html',Questions=DisplayQues(),get_Name=GetUserName)

@app.route('/Logout')
def Logout():
    session.pop('UserId',None)
    return render_template('Login.html')

@app.route('/Profile')
def Profile():
    return render_template('Profile.html',get_Mail=GetUserMail)

@app.route('/Answer/<int:Q_id>',methods=["POST","GET"])
def Answer(Q_id):
        return render_template('Answer.html',Ans_Com=GetAnswer())           

@app.route('/Question/<int:Q_id>',methods=["POST","GET"])
def Question(Q_id):
    if(request.method=="POST"):
        A_txt=request.form['A_text']
        An=int(request.form.get('anonymous',0))
        file=request.files['file']
        if(A_txt):
            A_id=InsertAns(Q_id,session['UserId'],A_txt,An)
            if(file):
                f_path=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
                file.save("static/"+f_path)
                InsertFiles(A_id,f_path)
        else:
            print("Answer is blank")
        return render_template('Question.html',Question=GetQuestion(Q_id),Get_File=GetFileLoc,get_Name=GetUserName)
    else:    
        return render_template('Question.html',Answer=GetQuestion(Q_id),Get_File=GetFileLoc,get_Name=GetUserName)

@app.route('/Question/UpVotes/<int:A_id>',methods=["POST","GET"])
def UpVote(A_id):
    pass
@app.route('/Question/DownVotes/<int:A_id>',methods=["POST","GET"])
def DownVote(A_id):
    pass

if __name__=="__main__":
    app.run(debug=True)