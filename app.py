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
  #time.sleep(1)
  return render_template("welcome.html")

#ContactUs Page
@app.route('/contactus',methods=['GET','POST'] )
def contactus():
  #time.sleep(1)
  return render_template("contactus.html")

#Login Page for Application 
@app.route('/login', methods=['GET','POST'])
def login():
  #time.sleep(1)  
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
    if record :
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
 
#Add new product
@app.route('/add_new_product',methods=['GET','POST'])
def add_new_product():

  if fetch_user_role(session['username'])==0:
    print("Inside permission 1")
    flash('You dont have a permission to add a new product.')
    return render_template('dashboard.html')
  else:
    print("Inside permission 1 or 2")
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
      return render_template('dashboard.html')
    
    
#Product List   
@app.route('/product_list', methods=['GET', 'POST'])
def product_list():
   cur = mysql.connection.cursor()
   cur.execute('select product_id, product_category, product_name, product_stock_quantity from products')
   productList = cur.fetchall()
   print(productList)
   cur.close()
   return render_template('product_list.html', productList = productList)
 

#Product Details List
@app.route('/product_details_page/<product_id>' , methods=['GET', 'POST'])
def product_details_page(product_id):
   cur = mysql.connection.cursor()
   cur.execute('select * from products where product_id = %s',(product_id,))
   productdetails=cur.fetchone()
   print(productdetails)
   cur.close()
   return render_template('product_details_page.html',productdetails=productdetails)


#update new product
@app.route('/update_product',methods=['GET','POST'])
def update_product():
  # fetching data from user 
  global barcode_value,p_barcode,available_stock
  
  if request.method=='GET':
    available_stock=0
    barcode_value=barcode_scanner.extract_barcode()
    p_barcode=barcode_value[0]
    cur = mysql.connection.cursor()
    cur.execute('select product_stock_quantity from products where product_id =%s ',(p_barcode,))
    stock_query_result=cur.fetchone()
    for i in stock_query_result:
      available_stock=i     
    print(available_stock)
    cur.close()
    return render_template('update_product.html',p_barcode=p_barcode)

  else:
    #product_stock_quantity =request.form['productstockquantity']
    cur = mysql.connection.cursor()
    new_stock = request.form['productstockquantity']
    cur.execute('update products set product_stock_quantity =%s where product_id=%s',(available_stock+int(new_stock),p_barcode))
    mysql.connection.commit()
    cur.close()
    flash("Added")
    return render_template('dashboard.html')

# customer details page
@app.route('/customer_details')
def customer_details():
  if request.method=='POST':
    customer_name= request.form['customername']
    customer_contact="+91"+request.form['customercontact']
    customer_email=request.form['customeremail']
    return render_template('customer_details.html')
  
  return render_template('customer_details.html')

# create bill
global billing_items
billing_items={}
@app.route('/create_bill',methods=['GET','POST'])
def create_bill():
  cur=mysql.connection.cursor()
  value=barcode_scanner.extract_barcode()
  if value[0] in billing_items:
    billing_items[value[0]]+=1
  else:
    cur.execute('select product_name, product_price from products where product_id =%s',(value[0],))
    billing_items[value[0]]=1
    r=cur.fetchall()  
    print(r)
    cur.close()
  print(billing_items)
   
  if request.method=='POST':
    print('inside post method')
    return render_template('create_bill.html',billing_items_barcodes=billing_items)
  return render_template('create_bill.html',billing_items_barcodes=billing_items)

#View employee List
@app.route('/employee_list', methods=['GET', 'POST'])
def employee_list():
   cur = mysql.connection.cursor()
   cur.execute('select user_id, user_role,user_username from users')
   employeeList = cur.fetchall()
   print(employeeList)
   cur.close()
   return render_template('employee_list.html', employeeList = employeeList)
 
#users details page
@app.route('/users_details_page/<user_id>' , methods=['GET', 'POST'])
def users_details_page(user_id):
   cur = mysql.connection.cursor()
   cur.execute('select * from users where user_id = %s',(user_id,))
   employeedetails=cur.fetchone()
   print(employeedetails)
   cur.close()
   return render_template('users_details_page.html',employeedetails=employeedetails)

#Resend otp page:
@app.route('/resend_otp')
def resend_otp():
   #otp.send_otp("+917757963133",created_otp)
   flash("New OTP Sent!! ")
   return redirect(url_for('otp_page'))
 
#profile page
@app.route('/profile/<username>',methods=['GET', 'POST'])
def profile(username):
  cur = mysql.connection.cursor()
  cur.execute('select user_fullname, user_role, user_contact, user_email from users where user_username = %s',(username,))
  user = cur.fetchone()
  cur.close()
 
  return render_template('profile.html', user = user)

#logout function  
@app.route('/logout', methods=['GET','POST'])
def logout():
   session.pop("username")
   session.pop("loggedin")
   return render_template("logout.html")

# function for fething user role for managing the permissions
def fetch_user_role(username):
  cur=mysql.connection.cursor()
  cur.execute('select user_role from users where user_username = %s',(username,))
  permission=cur.fetchone()
  cur.close()
  for user_role in permission:
    permission = user_role
    print("Permission : ",user_role)
  return permission


#To run the application
if __name__ == '__main__':
    app.run(debug=True)