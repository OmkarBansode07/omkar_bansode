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

otp_value = ""

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
    # logout()
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
        print("The user is =",session["username"])
        
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
# otp.send_otp("+917757963133",created_otp)

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
        return redirect(url_for('dashboard'))
     else:
        flash("Wrong OTP !! TRY AGAIN !!")
        return redirect(url_for('otp_page'))
     
     
  else:
     
     return render_template("otp_page.html")

#Dashboard page
@app.route('/dashboard')
def dashboard():
   #print('Dashboard = ', session["username"])
   username = session["username"]
   return render_template('dashboard.html', username = username)

#profile page
@app.route('/profile/<username>',methods=['GET', 'POST'])
def profile(username):
  cur = mysql.connection.cursor()
  cur.execute('select user_username, user_role, user_contact, user_email from users where user_username = %s',(username,))
  user = cur.fetchone()
  cur.close()
  
  return render_template('profile.html', user = user)

#View product List
@app.route('/product_list', methods=['GET', 'POST'])
def product_list():
   cur = mysql.connection.cursor()
   cur.execute('select product_id, product_category, product_name, product_stock_quantity from products')
   productList = cur.fetchall()
   print(productList)
   cur.close()
   return render_template('product_list.html', productList = productList)
   
#product_details_page
@app.route('/product_details_page/<product_id>' , methods=['GET', 'POST'])

def product_details_page(product_id):
   cur = mysql.connection.cursor()
   cur.execute('select * from products where product_id = %s',(product_id,))
   productdetails=cur.fetchone()
   print(productdetails)
   cur.close()
   return render_template('product_details_page.html',productdetails=productdetails)

#View employee List
@app.route('/employee_list', methods=['GET', 'POST'])
def employee_list():
   cur = mysql.connection.cursor()
   cur.execute('select user_id, user_role,user_username from users')
   employeeList = cur.fetchall()
   print(employeeList)
   cur.close()
   return render_template('employee_list.html', employeeList = employeeList)



#Resend otp page:
@app.route('/resend_otp')
def resend_otp():
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
