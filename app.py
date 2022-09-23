from flask import Flask,render_template,request,Response,session,redirect
import mysql.connector

import os
from datetime import date



app=Flask(__name__)

app.secret_key='shrishti'  #session key 

UPLOAD_FOLDER='./static/upl' #for image
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER 




@app.route("/")
def Home():  
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("select * from products")
    data=cur.fetchall()
    return render_template('home.html',item=data)                         
  
                              
@app.route("/a")
def adminlogin():       
    return render_template("adminlogin.html")   
#admin
@app.route('/code1',methods=['POST'])
def ad():
    email=str(request.form["t1"])
    pass1=str(request.form["t2"])
    conn=mysql.connector.connect(host='localhost', user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()

    cur.execute("select * from adminlogin where Email='"+email+"' and Password='"+pass1+"' ")

    if(cur.fetchone()):
        
        return render_template('adminhome.html')
    else:
        return render_template('adminlogin.html')


    
  
    
   
  

@app.route("/ah")
def adminhome():           
    return render_template("adminhome.html")

@app.route("/r")
def RestaurantRegistration():           
    return render_template("RestaurantRegistration.html")

@app.route("/code11",methods=["POST"])
def save():
    conn=mysql.connector.connect(host="localhost",user="root",password='root',database="onlinefoodorder")
    cur=conn.cursor()
    id=str(request.form["t1"])
    nam=str(request.form["t2"])
    address=str(request.form["t3"])
    email=str(request.form["t4"])
    mob=str(request.form["t5"])

    cur.execute("insert into restaurantregistration(Id,Name,Address,Email,MobileNo)values('"+id+"','"+nam+"','"+address+"','"+email+"','"+mob+"')")
    conn.commit()

@app.route("/i")
def Items():           
    return render_template("Items.html")

@app.route("/item",methods=["POST"])
def Item():
    if 'file1' not in request.files:
        return' there is no file in form'

    file1=request.files["file1"]
    path=os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file1.save(path)
    id=str(request.form["t1"])
    nam=str(request.form["t2"])
    price=str(request.form["t3"])
    Des=str(request.form["t4"])
    conn=mysql.connector.connect(host="localhost",user="root",password='root',database="onlinefoodorder")
    cur=conn.cursor()
                        

    cur.execute("insert into products(Id,Name,Price,Description,Image)values('"+id+"','"+nam+"','"+price+"','"+Des+"','"+file1.filename+"')")
    conn.commit()
    return redirect("/showdata")
  
 #data show    

@app.route("/show")
def sh():           
    return render_template("showtable.html")
@app.route("/showdata")
def data_show():
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("select * from products")
    data=cur.fetchall()
    return render_template('showtable.html',item=data)                

@app.route("/search",methods=["POST"]) 
def data_show1():
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    ser=str(request.form["se"])
    cur.execute("select * from products where Name = '"+ser+"' ")   
    data=cur.fetchall() 
    return render_template('showtable.html',item=data)   
                                                                                              

@app.route("/del")
def delete():
    id=request.args.get('Id')
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("delete from products where Id="+str(id))
    conn.commit()
    cur.execute("select * from products")
    data=cur.fetchall()
    return render_template('showtable.html',item=data)

@app.route("/edit")
def upd():
    id=request.args.get('Id')
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("select * from products where Id="+str(id))
    data=cur.fetchone()
    return render_template("update.html",data1=data)

@app.route("/alter",methods=["POST"])
def alt():
    id=str(request.form['Id'])
    Name=str(request.form['Name'])
    Price=str(request.form['Price'])
    desc=str(request.form['desc'])
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("update products set Name='"+Name+"',Price="+Price+",Description='"+desc+"'  where Id=" +id)
    conn.commit()
    return redirect('/showdata')

   #cart  

@app.route("/cart")
def ct():
    try:
        if session.get('UserName'):
            id=request.args.get("id")
            conn=mysql.connector.connect(host="localhost",user="root",password='root',database="onlinefoodorder")
            cur=conn.cursor()
            cur.execute("select * from products where Id="+str(id))
            data=cur.fetchone()
            return render_template("cart.html" ,data1=data)
        else:
            return render_template('error.html')
        

           
    except Exception as e:

        return render_template("error.html",ex=e)
    
          











@app.route("/j")
def jinga():
    return render_template("jinga.html")

@app.route("/u")
def UserRegistration():
    return render_template("UserRegistration.html")
#logout 
@app.route("/logout")
def log_out():
    session["UserName"]=''
    session['email']=''
   
    return redirect('/')
   

@app.route("/code2",methods=["POST"])
def Register():
    conn=mysql.connector.connect(host="localhost",user="root",password='root',database="onlinefoodorder")
    cur=conn.cursor()
    usernam=str(request.form["t1"])
    email=str(request.form["t2"])
    password=str(request.form["t3"])
    mob=str(request.form["t4"])
    add=str(request.form["t5"])

    cur.execute("insert into userregis(UserName,Email,Password,MobileNo,Address)values('"+usernam+"','"+email+"','"+password+"','"+mob+"','"+add+"')")
    conn.commit()
    return render_template("UserLogin.html")

@app.route("/ul")
def UserLogin():
    return render_template("UserLogin.html")



@app.route('/code3',methods=['POST'])
def log_info():
    email=str(request.form["t1"])
    pass1=str(request.form["t2"])
    conn=mysql.connector.connect(host='localhost', user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()

    cur.execute("select * from userregis where Email='"+email+"' and Password='"+pass1+"' ")

    if(cur.fetchone()):
        cur.execute("select * from userregis where Email='"+email+"' and Password='"+pass1+"' ")
        data=cur.fetchone()
        session["UserName"]=str(data[0])
        

        return redirect('/')
    else:
        return render_template('adminlogin.html')

@app.route("/pay")    
def pay():
    return render_template("payment.html")                     

@app.route('/payment',methods=["POST"])
def paydetails():

    FullName=str(request.form['fname'])
    Email=str(request.form['em'])
    Address=str(request.form['ed'])
    City=str(request.form['City'])
    State=str(request.form['st'])
    Zipcode=str(request.form['code'])
    NameonCard=str(request.form['card'])
    cardn=str(request.form['Credit'])
    emonth=str(request.form['Exp'])
    eyear=str(request.form['Year'])
    cvv=str(request.form['Cvv'])
    date1=date.today()
    d1=date1.strftime("%d/%m/%Y")



    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("insert into payment(FullName,Email,Address,City,State,Zipcode,NameonCard,cardn,emonth,eyear,cvv,date1)values('"+FullName+"','"+Email+"','"+Address+"','"+City+"','"+State+"','"+Zipcode+"','"+NameonCard+"','"+cardn+"','"+emonth+"','"+eyear+"','"+cvv+"' , '"+d1+"')")
    conn.commit()
    return 'success'


@app.route("/s")    
def ss():
    conn=mysql.connector.connect(host='localhost',user='root',password='root',database='onlinefoodorder')
    cur=conn.cursor()
    cur.execute("select * from payment")
    data=cur.fetchall()
    return render_template('show.html',item=data)       

@app.route("/res")        
def rest():
    return render_template("Restaurantsearch.html")                   

if __name__=='__main__':
    app.run(debug=True)   

