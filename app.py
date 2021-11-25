from flask import Flask,render_template,redirect,request,session
from flask_mail import Mail, Message
from datetime import datetime
from Sql_Querries import CheckUser,CheckMail,CheckLogin, DisplayAnsUser, DisplayQuesUser, GetQuestion, Getemail, InsertAns, InsertQues,InsertUser,DisplayQues,GetUserId

app=Flask(__name__)
app.secret_key = "cn assignment safty key **&**"
mail = Mail(app)

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
        return render_template('Home.html',Questions=DisplayQues())    
    if(not session.get('UserId',None)):
        return render_template('Login.html')
    else:
        return render_template('Home.html',Questions=DisplayQues())

@app.route('/Logout')
def Logout():
    session.pop('UserId',None)
    return render_template('Login.html')

@app.route('/Profile')
def Profile():
    return render_template('Profile.html',data=Getemail(session['UserId']))

@app.route('/Profile/questions')
def ProfileQue():
    dataq = DisplayQuesUser(session['UserId'])
    return render_template('UserQuestionList.html',data=dataq)

@app.route('/Profile/answers')
def ProfileAns():
    dataa = DisplayAnsUser(session['UserId'])
    return render_template('UserAnswerList.html',data=dataa)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xyz@gmail.com' # _________________ADD YOUR EMAIL ID AND PASSWORD _____________
app.config['MAIL_PASSWORD'] = '******' # _______________ADD YOUR EMAIL ID AND PASSWORD __________________
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False

mail = Mail(app)

@app.route('/Answer/<int:Q_id>',methods=["POST"])
def Answer(Q_id):
    if(request.method=="POST"):
        A_txt=request.form['A_text']
        if(A_txt):
            user = InsertAns(Q_id,session['UserId'],A_txt)
            r = Getemail(int(user[0]))
            msg = Message( 'Hello from mini-quora!', sender ='chiluverupreeti@gmail.com', recipients = [str(r[0])])
            msg.body = 'Hello!! You got a message from Mini-quora! Your question has been answered'
            mail.send(msg)
        else:
            print("Answer is blank")
        return render_template('Question.html',Answer=GetQuestion(Q_id))        
        

@app.route('/Question/<int:Q_id>',methods=["POST","GET"])
def Question(Q_id):
    return render_template('Question.html',Answer=GetQuestion(Q_id))


if __name__=="__main__":
    app.run(debug=True)
