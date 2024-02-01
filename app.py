from flask import Flask, render_template, redirect, request, url_for ,session,redirect ,flash
from flask_mysqldb import MySQL
from adapter import otp
import time


app = Flask(__name__)
app.secret_key = ("superkey")

app.config["SESSION_PERMANENT"] = False
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "inventory"
mysql = MySQL(app)



#Welcome Page
@app.route('/')
def welcome():
  
  
  return render_template("welcome.html")

#ContactUs Page
@app.route('/contactus',methods=['GET','POST'] )
def contactus():
  return render_template("contactus.html")



# Index Page for test

@app.route('/index', methods=['GET','POST'] )
def index():
  if len(session) == 0:
    return render_template("login.html")
  else:
    return render_template("index.html", username = session["username"])


#Login Page for Application 
@app.route('/login', methods=['GET','POST'])
def login():
  msg = ''
  
  record = ""
  print(session)

  if len(session) > 0:
    print("session")
    # redirect(url_for('logout'))
    logout()
  print(session)
  
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute('select * from users where user_username =%s and user_password = %s',(username, password,))
    record = cur.fetchone()
    print("LOG: record user-m:Post:", record)
    if record:
        print("LOG: record user:", record) 
        #Session start
        

        
        session['loggedin'] = True
        session["username"] = username
        cur = mysql.connection.cursor()
        cur.execute('select user_contact from users where user_username = %s',(session['username'],))
        user_contact_fromdb=cur.fetchone()
        for user_contact in user_contact_fromdb:
          print(user_contact)
        print("The user is =",session["username"])

        print("user contact is : ",user_contact)
        global created_otp
        created_otp = otp.generate_otp()

        
        otp.send_otp(user_contact,created_otp)
        
        return redirect(url_for('otp_page'))
    
    else:
        print("else")
        flash("incorrect username password")
        return render_template('login.html') 
  else:
     
     return render_template('login.html')

def s_user():
  u = session['username']
  print(u)

#OTP Page for application

created_otp= otp.generate_otp()



@app.route('/otp_page',methods= ['GET','POST'])
def otp_page():
  print(created_otp)
  #print(created_otp,created_otp[-5::])
  

  
  if request.method == "POST":
     print(request.form["otp"])
     print(request.form["otp"] in created_otp[-5::]  )
     print(type(created_otp[-5::]),type(request.form["otp"]))


     if request.form["otp"] in created_otp:
        # username = session['username'] 
        return redirect(url_for('Dashboard'))
     else:
        flash("Wrong OTP !! TRY AGAIN !!")
        
        return redirect(url_for('otp_page'))
     
     
  else:
     
     return render_template("otp_page.html")


#Dashboard Page
@app.route('/Dashboard')
def Dashboard():
   print('Dashboard = ',session["username"])
   return render_template('Dashboard.html')

#Resend otp page:
@app.route('/resend_otp')
def resend_otp():
   #otp.send_otp("+917757963133",created_otp)
   flash("New OTP Sent!! ")
   return redirect(url_for('otp_page'))


#logout function  
@app.route('/logout', methods=['POST'])
def logout():
   session.pop("username")
   session.pop("loggedin")
   return redirect(url_for("login"))

#To run the application
if __name__ == '__main__':
    app.run(debug=True)
