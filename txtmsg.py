import sqlite3
import sys
from twilio.rest import Client
def send_text_visitor(name,host,stuff,phone,timenow):
    message = "Hi," + name + "\nYour meeting with " + host + " started at " + timenow + ".\nEnd your meeting at - http://127.0.0.1:5000" + stuff + " ."
    client = Client("AC222e4838d657fd4fe0517a91d637e6e8", "6c260eac51666b46067dd07d807ff99a")
    client.messages.create(to="+91"+phone, from_="+12018015038",body=message)
    print(phone,file=sys.stderr)
def send_text_visitor_2(name):
    with sqlite3.connect("first.db") as con:
        cur = con.cursor()
        cur2=con.cursor()
        cur.execute("SELECT host,timestart,timeend FROM totallog WHERE visitor=(?)",(name,))
        answer=cur.fetchone()
        cur2.execute("SELECT address,phone FROM hosts WHERE name=(?)",(answer[0],))
        answer2=cur2.fetchone()
        cur2.execute("SELECT visitor_phone FROM totallog WHERE visitor=(?)",(name,))
        answer3=cur2.fetchone()
    print(answer3)
    message = "Details of meeting.\n Name of Host : " + answer[0] + "\n" + "Check-In Time : " + answer[1] + "\nCheck-Out Time : " + answer[2] +"\nAddress :"+answer2[0]+"\nPhone :"+str(int(answer2[1]))
    client = Client("AC222e4838d657fd4fe0517a91d637e6e8","6c260eac51666b46067dd07d807ff99a")
    client.messages.create(to="+91"+str(int(answer3[0])),from_="12018015038",body=message)
    # print(answer2[1],file=sys.stderr)
def send_text_host_start(name,host,visem,time_date,timestart):
    with sqlite3.connect("first.db") as con:
        cur=con.cursor()
        cur.execute("SELECT phone FROM hosts WHERE name=(?)",(host,))
        phone=cur.fetchone()[0]
        cur.execute("SELECT visitor_phone FROM visit where visitor=(?)",(name,))
        visitpho = cur.fetchone()[0]
    message = 'You have a Visitor! \n Name : {}\n Email : {}\n Phone : {}\nTime : {}\n Date : {}'.format(name,visem,str(int(visitpho)),timestart,time_date)
    client = Client("AC222e4838d657fd4fe0517a91d637e6e8","6c260eac51666b46067dd07d807ff99a")
    client.messages.create(to="+91"+str(int(phone)),from_="12018015038",body=message)
    print(phone,file=sys.stderr)
def send_text_host_start_chat(name,host,visem,time_date,timestart,chatlink):
    with sqlite3.connect("first.db") as con:
        cur=con.cursor()
        cur.execute("SELECT phone FROM hosts WHERE name=(?)",(host,))
        phone=cur.fetchone()[0]
    message = 'You have a Visitor! \n Name : {}\n Email : {}\n Time : {}\n Date : {}\nChat with him! :{}'.format(name,visem,timestart,time_date,chatlink)
    client = Client("AC222e4838d657fd4fe0517a91d637e6e8","6c260eac51666b46067dd07d807ff99a")
    client.messages.create(to="+91"+str(int(phone)),from_="12018015038",body=message)
    print(phone,file=sys.stderr)
