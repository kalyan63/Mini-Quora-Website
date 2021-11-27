from flask import Flask,render_template,redirect,request,session
from datetime import datetime
from Sql_Querries import Check_Follow, CheckUser,CheckMail,CheckLogin,\
FollowUser, GetFileLoc, InsertFiles,InsertUser,DisplayQues,GetUserId,\
GetUserDetails,GetUserMail,GetUserQues,GetUserAns,GetFollowId,InsertQues,GetQuestion,GetAnswer,InsertAns,\
GetUserName, UnfollowUser,UserVoteAns,InsertCom,InsertFiles,GetFileLoc
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

@app.route('/profile/<int:user_Id>')
def Profile(user_Id):
    if(user_Id!=session['UserId']):
        return render_template('Profile.html',user=GetUserDetails(user_Id),foll=Check_Follow(session['UserId'],user_Id))
    else:    
        return render_template('Profile.html',user=GetUserDetails(user_Id),get_Name=GetUserName,F_ID=GetFollowId(user_Id))

@app.route('/profile/follow/<int:user_Id>')
def Follow(user_Id):
    FollowUser(session['UserId'],user_Id)
    return render_template('Profile.html',user=GetUserDetails(user_Id),foll=Check_Follow(session['UserId'],user_Id))

@app.route('/profile/unfollow/<int:user_Id>')
def UnFollow(user_Id):
    UnfollowUser(session['UserId'],user_Id)
    return render_template('Profile.html',user=GetUserDetails(user_Id),foll=Check_Follow(session['UserId'],user_Id))

@app.route('/profile/Question/<int:user_id>')
def UserQuestionList(user_id):
    Aut=[]
    Aut.append(session['UserId']==user_id)
    Aut.append(GetUserName(user_id))
    return render_template('UserQuestionList.html',Questions=GetUserQues(user_id),Aut=Aut)

@app.route('/profile/Answer/<int:user_id>')
def UserAnswerList(user_id):
    Aut=[]
    Aut.append(session['UserId']==user_id)
    Aut.append(GetUserName(user_id))
    return render_template('UserAnswerList.html',Answers=GetUserAns(user_id),Aut=Aut)

@app.route('/Answer/<int:A_id>',methods=["POST","GET"])
def Answer(A_id):
    if(request.method=="POST"):
        C_Text=request.form['C_text']
        An=int(request.form.get('anonymous',0))   
        user_id=session['UserId']
        if(C_Text):
            InsertCom(A_id,user_id,C_Text,An)
        else:
            print("Please enter a question") 
        return render_template('Answer.html',Ans_Com=GetAnswer(A_id),Get_File=GetFileLoc,get_Name=GetUserName)     
    else:
        return render_template('Answer.html',Ans_Com=GetAnswer(A_id),Get_File=GetFileLoc,get_Name=GetUserName)          

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
        return render_template('Question.html',Question=GetQuestion(Q_id),Get_File=GetFileLoc,get_Name=GetUserName)

@app.route('/Question/UpVotes/<int:A_id>',methods=["POST","GET"])
def UpVote(A_id):
    UserVoteAns(session['UserId'],A_id,1)
    return render_template('Answer.html',Ans_Com=GetAnswer(A_id),Get_File=GetFileLoc,get_Name=GetUserName)

@app.route('/Question/DownVotes/<int:A_id>',methods=["POST","GET"])
def DownVote(A_id):
    UserVoteAns(session['UserId'],A_id,0)
    return render_template('Answer.html',Ans_Com=GetAnswer(A_id),Get_File=GetFileLoc,get_Name=GetUserName)

if __name__=="__main__":
    app.run(debug=True)