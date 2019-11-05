import requests
import json
import aiml
from sqlite3 import connect
import webbrowser


conn = connect("conv.db",timeout=10)
sql='create table if not exists '+'conversation'+'(id INT,user TEXT,bot TEXT)'
sql2='create table if not exists '+'user_details'+'(user_name TEXT NOT NULL,phone_number INTEGER NOT NULL,Product_name TEXT NOT NULL,status TEXT NOT NULL,price INTEGER,condition TEXT)'
conn.execute(sql)
conn.execute(sql2)
conn.commit()
#conn2.commit()
cursor=conn.execute('SELECT id from conversation')
id=0
for items in cursor:
	id=items[0]
id=id+1
def insert(u,b):
	conn.execute("INSERT INTO conversation (id,user,bot) VALUES (?,?,?) ",(id,u,b))
	conn.commit()
kernel=aiml.Kernel()
kernel.learn("bot/start.aiml")
kernel.respond("learn ai")


while True:
    u=input(">>>")
    if str(u)[:6]=="google" or str(u)[:6]=="Google":
        url = "https://www.google.com.tr/search?q={}".format(str(u)[6:]);    
        webbrowser.open(url,2)
        insert(str(u),"")
        continue;
    s=kernel.respond(u)
#    print(s)
#    print(s)
    if s == "Sell" :
        print("Enter your name : " )
        name1 = input()
        print("Enter your Phone Number")
        numb = input()
        print("Enter the product name : ")
        pname = input()
        pname = pname.lower()
        pname = pname.replace(" ","")
        print("Enter the Selling price :" )
        p = input()
        print( "Condition of the product " )
        co = input()
        conn.execute("INSERT INTO user_details (user_name,phone_number,Product_name,status,price,condition) VALUES (?,?,?,?,?,?) ",(name1,numb,pname,"Sell",p,co))
#        conn.commit()
        conn.commit()
        cur = conn.cursor()
        cur.execute("SELECT user_name , phone_number from user_details where status = 'Buy' AND Product_name =?",(pname,) )
        conn.commit()
        rows = cur.fetchall()
        if len( rows) == 0:
            print("Currently nobody wants to buy your product ")
        else: 
            print ( "The details of the people who want to buy are : " )
            for row in rows:
                n,num = row
                print("Name : ",n ,"\nContact  : ",num)
        continue
    elif s == "Buy" :
        print("Enter your name : " )
        name1 = input()
        print("Enter your Phone Number")
        numb = input()
        print("Enter the product name : ")
        pname = input()
        pname = pname.lower()
        pname = pname.replace(" ","")
        conn.execute("INSERT INTO user_details (user_name,phone_number,Product_name,status,price,condition) VALUES (?,?,?,?,?,?) ",(name1,numb,pname,"Buy","",""))
        conn.commit()
        cur = conn.cursor()
        cur.execute("SELECT user_name , phone_number , price,condition from user_details WHERE status = 'Sell' AND Product_name =?",(pname,) )
        conn.commit()
        rows = cur.fetchall()
        if len(rows) == 0:
             print("Currently nobody is selling the product ..")
             print("Your request has been submitted")
        else: 
            print ( "The details of the sellers are : " )
            for row in rows:
                n,num,p,co = row
                print("Name : ",n ,"\nContact  : ",num,"\nPrice :",p,"\nCondition :",co)
        continue
    elif s=="Show":
        print("Enter your name : " )
        name1 = input()
        cur = conn.cursor()
        cur.execute("SELECT Product_name from user_details WHERE status = 'Sell' AND user_name =?",(name1,) )
        conn.commit()
        rows = cur.fetchall()
        if len(rows) == 0:
             print("Currently you have no sell requests")
             
        else: 
            print ( "The  products which you are selling  are : " )
            for row in rows:
                n= row
                print("Product Name : ",n[0],"\n" )
        cur.execute("SELECT Product_name from user_details WHERE status = 'Buy' AND user_name =?",(name1,) )
        conn.commit()
        rows = cur.fetchall()
        if len(rows) == 0:
             print("Currently you have no buy requests")
             
        else: 
            print ( "The  products which you want to buy are : " )
            for row in rows:
                n= row
                print("Product Name : ",n[0] )
        continue

    s=s.split('newline')
    ch=False
    v=""
    for item in s:
        print(str(item))
        v=v+str(item)
        if 'Bye' in item:
            ch=True
    insert(u,v)
    if ch :
        break
