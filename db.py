import sqlite3

def connection():
    try:
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        table1="create table accounts(account_no integer primary key autoincrement,username text ,password text,dob text,email text,contact float,gender text,account_type text,account_bal float)"
        table2="create table txn(account_no integer,account_bal float,updata_bal float,txn_type text,date text,to_account integer)"
        cur.execute(table2)
        cur.execute(table1)
        con.commit()
        con.close()  
        return ("Tables created")
    except:
        return ("something went wrong in db,might be tabl(s) already exists")

