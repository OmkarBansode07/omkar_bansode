from flask import Flask, render_template, redirect, request, url_for ,session,redirect ,flash
from flask_mysqldb import MySQL
from adapter import otp,barcode_scanner
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
        cur.close()

        
        #otp.send_otp(user_contact,created_otp)
        
        return redirect(url_for('otp_page'))
    
    else:
        print("else")
        flash("incorrect username password")
        return render_template('login.html') 
  else:
     
     return render_template('login.html')

#Session user
def s_user():
  u = session['username']
  print(u)

#OTP Page for application
#created_otp= otp.generate_otp()
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

#Dashboard Page
@app.route('/dashboard')
def dashboard():
   print('Dashboard = ',session["username"])
   return render_template('dashboard.html')
 
 #Add New product

#Add new product
@app.route('/add_new_product',methods=['GET','POST'])
def add_new_product():
  # fetching data from user 
  global barcode_value,p_manu_code,p_cate_code,p_name_code,p_barcode

  if request.method=='GET':
    barcode_value=barcode_scanner.extract_barcode()
    p_barcode=barcode_value[0]
    p_manu_code =  barcode_value[2]
    p_cate_code = barcode_value[1]
    p_name_code = barcode_value[4]
    return render_template('add_new_product.html',p_barcode=p_barcode,p_manu_code=p_manu_code,p_cate_code=p_cate_code,p_name_code=p_name_code)

  else:
    product_manufacturer =request.form['productmanufacturer']
    product_category=request.form['productcategory']
    product_name =request.form['productname']
    product_price =request.form['productprice']
    product_expirydate =request.form['productexpirydate']
    product_size =request.form['productsize']
    product_mfg =request.form['productmanufacturedate']
    product_measure =request.form['productmeasure']
    product_stock_quantity =request.form['productstockquantity']
    print("barcode value from api : ",barcode_value)
    cur = mysql.connection.cursor()
    cur.execute('insert into products values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(p_barcode,product_manufacturer,p_manu_code,product_category,p_cate_code,product_name,p_name_code,product_price,product_measure,product_size,product_expirydate,product_mfg,product_stock_quantity))
    mysql.connection.commit()
    cur.close()
    flash("Added")
    return render_template(dashboard)

#update new product
@app.route('/update_product',methods=['GET','POST'])
def update_product():
  # fetching data from user 
  global barcode_value,p_barcodes

  if request.method=='GET':
    barcode_value=barcode_scanner.extract_barcode()
    p_barcode=barcode_value[0]
    return render_template('update_product.html',p_barcode=p_barcode)

  else:
    #product_stock_quantity =request.form['productstockquantity']
    cur = mysql.connection.cursor()
    cur.execute('update products set product_stock_quantity =%s where product_id=%s',(12,p_barcode))
    mysql.connection.commit()
    cur.close()
    flash("Added")
    return render_template('dashboard.html')

# remove product
@app.route('/create_bill',methods=['GET','POST'])
def create_bill():
  if request.method=='POST':
    return render_template('create_bill.html')
  return render_template('create_bill.html')

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