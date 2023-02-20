from flask import Flask,render_template,url_for,request,send_file,redirect,flash,get_flashed_messages
import sqlite3
import os
import re
import db
import random
from datetime import datetime
import pandas as pd



#intilize frame
app=Flask(__name__,static_url_path='/static')



app.secret_key = 'random string'
#connection to databaseand create
connection=db.connection()
print(connection)


# for all 
@app.route("/")
@app.route("/home")
def home():
    return render_template("/before login/home.html",page="home")


#loginpage
@app.route("/loginpage")
def loginpage():
    return render_template("/before login/loginpage.html")

#create account
@app.route("/create_account")
def create_account():
    return render_template("/before login/create_account.html")

#service page
@app.route("/services")
def service():
    return render_template("/before login/services.html")

#contact page
@app.route("/contact")
def contact():
    return render_template("/before login/contactus.html")

@app.route("/trt")
def trt():

    return render_template("/after login/transaction_history.html")

@app.route("/help")
def help():
    f=open("help/aaaa..txt",'r')
    f.seek(0)
    data=f.readlines()
    li=list()
    for i in data:
        i=re.sub(">","",i)
        li.append(i)
        
    f.close()
    
    return render_template("before login/help.html",data=li)





#loginform
@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        account_no=request.form['account_no']
        password=request.form['password']
        print(account_no,password)
        
        if(account_no=="" or password==""):
            return render_template('/before login/loginpage.html',error="invalid account_no and password")
        else:
            #connect form to sql
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=? and password=?",(account_no,password))
            global tup
            tup=cur.fetchone()
            if(tup==None):
                return render_template('/before login/loginpage.html',error="invalid account_no and password")
            else:
                
                return render_template('userpage.html',username=tup[1])
            





@app.route('/account_open', methods=['POST', 'GET'])
def account_open():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']

        email = request.form['email']
        contact = request.form['contact_no']
        account_type = request.form['account_type']
        gender = request.form['gender']
       
        if username == "" or password == "" or dob == "" or email == "" or contact == "" or gender == "":
            return render_template("/before login/create_account.html", error="invalid data")
       
            

            
        else:
            if account_type=="Current":
                account_bal=1000
            else:
                account_bal=2000
            global userdata
            userdata=dict(username=username,password=password,dob=dob,email=email,contact=contact,gender=gender,account_type=account_type,account_bal=account_bal)
            global list
            list = ""
            for _ in range(4):
                i = random.randint(1,9 )
                list = list+str(i)+""
            flash(f"you otp is {list}")

            return redirect(url_for('varification'))


@app.route("/varification")
def varification():
    return render_template("/before login/otp.html")

@app.route("/otp",methods=['POST','GET'])
def otp():
    if request.method=="POST":
        otp=request.form['otp']
        if(otp==list):
            username=userdata["username"]
            password=userdata["password"]
            dob=userdata["dob"]
            email=userdata["email"]
            contact=userdata["contact"]
            account_type=userdata["account_type"]
            gender=userdata["gender"]
            account_bal=userdata["account_bal"]


            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("insert into accounts(username,password,dob,email,contact,gender,account_type,account_bal) values(?,?,?,?,?,?,?,?)",(username,password,dob,email,contact,gender,account_type,account_bal))
            con.commit()
            con.close()

            #get the account number
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select max(account_no) from accounts")
            tup=cur.fetchone()
            con.close()


            dir = "userinformation"

            # changes the current directory to
            # Sibling_2 folder
            os.chdir(dir)
            f = open(f"{tup[0]}.txt", "w")
            f.write(f"""
            **********sbi bank***************
            account_no->{tup[0]}
            username->{username}
            password->{password}
            email->{email}
            contact->{contact}
            dob->{dob}
            gender->{gender}
            account_type->{account_type}
            account_bal->{account_bal}
            ********************************
            """)
            f.close()
            dir ="banking_web"
            os.chdir(dir)
            # opening file.txt which is to read
        




            return render_template('/before login/validation.html',account_no=tup[0],username=username,password=password,dob=dob,email=email,contact=contact,gender=gender,account_type=account_type,account_bal=account_bal)


        else:
            return render_template("/before login/otp.html",error="invalid data")









#after login 

@app.route("/userpage")
def userpage():
    return render_template('userpage.html',username=tup[1])



#service page
@app.route("/servicesforuser")
def servicesforuser():
    return render_template("/after login/servicesforuser.html")

#contact page
@app.route("/contactforuser")
def contactforuser():
    return render_template("/after login/contactforuser.html")


@app.route("/logout")
def logout():

    return redirect(url_for('home'))
 



@app.route("/helpforuser")
def helpforuser():
    f=open("help/aaaa..txt",'r')
    f.seek(0)
    data=f.readlines()
    li=list()
    for i in data:
        i=re.sub(">","",i)
        li.append(i)
        
    f.close()
    
    return render_template("after login/help.html",data=li)


@app.route("/transfermoney")
def transfermoney():
    return render_template("/after login/transfermoney.html",username=tup[1])

@app.route("/transfer",methods=['POST'])
def transfer():
   
    to_account_no=request.form["to_account_no"]
    ammount=int(request.form["ammount"])
    if int(to_account_no)==int(tup[0]):
        return render_template("/after login/transfermoney.html",username=tup[1],error="use onther account")
    else:
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select account_bal from accounts where account_no=?",(to_account_no,))
        amt=cur.fetchone()
        con.close()

        if(amt==None):
            return render_template("/after login/transfermoney.html",username=tup[1],error="account no will not found")
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
            bal=cur.fetchone()
            con.close()
            bal=int(bal[0])
            amt=int(amt[0])
            if(bal<ammount):
                return render_template("/after login/transfermoney.html",username=tup[1],error="insufficent balance")
            else:             
                try:
                    dt=str(datetime.now())
                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?,?)",(tup[0],bal,bal-ammount,"Send",dt,to_account_no))
                    cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(ammount,tup[0]))         
                    con.commit()
                    con.close()

                    con=sqlite3.connect(database="bank.sqlite")
                    cur=con.cursor()
                    cur.execute("insert into txn values(?,?,?,?,?,?)",(to_account_no,amt,amt+ammount,"Recive",dt,tup[0]))
                    cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(ammount,to_account_no))         
                    con.commit()
                    con.close()
                   
                    return render_template("/after login/transfermoney.html",username=tup[1],error=(f"you will transfer  {ammount}₹ to account no {to_account_no}"))

                except:
                    return render_template("/after login/transfermoney.html",username=tup[1],error=(f"server not running"))


#debit money
@app.route("/debitmoney")
def debitmoney():
    return render_template("/after login/debitmoney.html",username=tup[1])
               

@app.route("/debit",methods=['POST'])
def debit():
                amt=int(request.form["ammount"])
                if amt<=0:
                    
                    return render_template("/after login/debitmoney.html",error="invalid value",username=tup[1])
                else:
                    txn_type="Widrow"
                    try:
                        dt=str(datetime.now())
                        con=sqlite3.connect(database="bank.sqlite")
                        cur=con.cursor()
                        cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
                        bal=cur.fetchone()[0]
                        con.close()
                        
                        con=sqlite3.connect(database="bank.sqlite")
                        cur=con.cursor()
                        cur.execute("insert into txn values(?,?,?,?,?,?)",(tup[0],bal,bal+amt,txn_type,dt,"NULL"))
                        cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,tup[0]))         
                        con.commit()
                        con.close()
                        
                        fl=(f"ammount of {amt} ruppes has been debited")
                        return render_template("/after login/debitmoney.html",error=fl,username=tup[1])
                    except:
                        
                        fl=(f"sorry ammount of {{amt}} ruppes has been not  debited")
                        return render_template("/after login/debitmoney.html",error=fl,username=tup[1])


#credit/widrow money

@app.route("/creditmoney")
def creditmoney():
    return render_template("/after login/creditmoney.html",username=tup[1])

@app.route("/credit",methods=['POST'])
def credit():
                amt=int(request.form["ammount"])
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
                bal=cur.fetchone()[0]
                con.close()
                if amt<=0:
                    
                    return render_template("/after login/creditmoney.html",error="invalid value",username=tup[1])
                elif amt>1000:
                    return render_template("/after login/creditmoney.html",error="only less than 1000 rs is widrow",username=tup[1])
                elif amt>bal:
                    return render_template("/after login/creditmoney.html",error="inseffeciant balance",username=tup[1])

                else:
                    txn_type="Credit"
                    try:
                        dt=str(datetime.now())
                        
                        con=sqlite3.connect(database="bank.sqlite")
                        cur=con.cursor()
                        cur.execute("insert into txn values(?,?,?,?,?,?)",(tup[0],bal,bal-amt,txn_type,dt,"NULL"))
                        cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,tup[0]))         
                        con.commit()
                        con.close()
                        
                        fl=(f"ammount of {amt} ruppes has been widrow")
                        return render_template("/after login/creditmoney.html",error=fl,username=tup[1])
                    except:
                        
                        fl=(f"sorry ammount of {{amt}} ruppes has been not  widrow")
                        return render_template("/after login/creditmoney.html",error=fl,username=tup[1])


#check balance
@app.route("/check_balance")
def check_balance():
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select account_bal from accounts where account_no=?",(tup[0],))
    tup2=cur.fetchone()
           
    con.close()
    return render_template("/after login/check_balance.html",username=tup[1],balance=tup2[0])






#update account
@app.route("/update_account")
def update_account():
    username=tup[1]
    password=tup[2]
    dob=tup[3]
    email=tup[4]
    contact=tup[5]
    return render_template("/after login/update_account.html",username=username,password=password,email=email,dob=dob,contact=contact)


@app.route("/update_data",methods=['POST','GET'])
def updata_data():
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        email = request.form['email']
        contact = request.form['contact_no']
        
        try:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("update accounts set username=?,password=?,dob=?,email=?,contact=? where account_no=?",(username,password,dob,email,contact,tup[0]))
            con.commit()
            con.close()


            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select gender,account_type,account_bal from accounts where account_no=?",(tup[0],))
            tup2=cur.fetchone()
           
            con.close()
            f=open(f"userinformation\\{tup[0]}.txt",'a')
            f.write(f"""

            *******updated account profile********

            account_no->{tup[0]}
            username->{username}
            password->{password}
            email->{email}
            contact->{contact}
            dob->{dob}
            gender->{tup2[0]}
            account_type->{tup2[1]}
            account_bal->{tup2[2]}

            ***********************************
            """)
            f.close()
            return render_template('/after login/validation.html',account_no=tup[0],username=username,password=password,dob=dob,email=email,contact=contact,gender=tup2[0],account_type=tup2[1],account_bal=tup[2])
        except:
            fl=("sorry profile in not updated try again later")
            username=tup[1]
            password=tup[2]
            dob=tup[3]
            email=tup[4]
            contact=tup[5]
            return render_template("/after login/update_account.html",error=fl,username=username,password=password,email=email,dob=dob,contact=contact)



#check balance
@app.route("/transaction_history")
def transaction_history():
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from txn where account_no=?",(tup[0],))
    txn=cur.fetchall()
    con.close()
    return render_template("/after login/transaction_history.html",username=tup[1],txn=txn)



@app.route("/profile")
def profile():
    account_no=tup[0]
    username=tup[1]
    password=tup[2]
    dob=tup[3]
    email=tup[4]
    contact=tup[5]
    gender=tup[6]
    account_type=tup[7]
    return render_template("/after login/profile.html",username=username,password=password,email=email,dob=dob,contact=contact,gender=gender,account_type=account_type,account_no=account_no)


#invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("/error page/404.html"), 404

#internal server
@app.errorhandler(500)
def page_not_found(e):
    return render_template("/error page/500.html",error="server not running"), 500






@app.route('/download')
def download_file():
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select max(account_no),username from accounts")
    tup=cur.fetchone()
    con.close()
    
    p=f"userinformation\\{tup[0]}.txt"
    return send_file(p,as_attachment=True)

@app.route('/updateprofile')
def update_profile():
    p=f"userinformation\\{tup[0]}.txt"
    return send_file(p,as_attachment=True)

@app.route('/get_trans_history')
def get_trans_history():
    con=sqlite3.connect(database="bank.sqlite")
    cur=con.cursor()
    cur.execute("select * from txn where account_no=?",(tup[0],))
    txn=cur.fetchall()
    con.close()
    d=[]
    for i in txn:
        d.append({"date":i[4],"transaction_type":i[3],"balance":i[1],"updated_bal":i[2],"toaccount":i[5]})
            
    df=pd.DataFrame(d)

    df.to_excel("userinformation\\transfer.xlsx")
    p="userinformation\\transfer.xlsx"
    return send_file(p,as_attachment=True)







if __name__=="__main__":
    app.run(debug=True)
