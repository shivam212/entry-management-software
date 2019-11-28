import smtplib
import sqlite3
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import gmtime, strftime
from sqlite3 import Error
from string import Template
MY_ADDRESS = 'managerentry@gmail.com'
PASSWORD = 'timepass9'
def send_visitor(name,host,stuff,email,timenow):
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart()
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting'
	message = "Hi," + name + "\nYour meeting with " + host + " started at,\nDate and Time : " + timenow + ".\nEnd your meeting at - http://127.0.0.1:5000" + stuff + " ."
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()
def send_visitor_chat(name,host,stuff,email,timenow,chatlink):
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart()
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting'
	message = "Hi," + name + "\nYour meeting with " + host + " started at " + timenow + ".\nThe Chat Link is http://127.0.0.1:5000"+ chatlink + ".\nEnd your meeting at - " + stuff + " ."
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()		
def send_visitor_2(name,email):
	with sqlite3.connect("first.db") as con:
		cur = con.cursor()
		cur2 = con.cursor()
		cur.execute("SELECT host,timestart,timeend FROM totallog WHERE visitor=(?)",(name,))
		answer = cur.fetchone()
		cur2.execute("SELECT address,phone FROM hosts WHERE name=(?)",(answer[0],))
		answer2 = cur2.fetchone()
		print((answer), file=sys.stderr)
		print((answer2), file=sys.stderr)
		# con.commit()
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart()
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting with ' + answer[0]
	message = "Details of meeting.\n Name of Visitor : " + name + "\n" + "Check-In Time : " + answer[1] + "\nCheckOut Time : " + answer[2] +"\nAddress :"+answer2[0]+"\nPhone :"+str(int(answer2[1]))
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()
def send_host_start(name,host,visem,time_date,timestart):
	with sqlite3.connect("first.db") as con:
		cur = con.cursor()
		cur.execute("SELECT email FROM hosts WHERE name=(?)",(host,))
		email = cur.fetchone()[0]
		# print(email, file=sys.stderr)
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart()
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']="New Visitor"
	message = 'You have a Visitor! \n Name : {}\n Email : {}\n Time : {}\n Date : {}'.format(name,visem,timestart,time_date)
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg 
def send_host_start_chat(name,host,visem,time_date,timestart,chatlink):
    with sqlite3.connect("first.db") as con:
        cur=con.cursor()
        cur.execute("SELECT email FROM hosts where name=(?)",(host,))
        email = cur.fetchone()[0]
        cur.execute("SELECT visitor_phone FROM visit where visitor=(?)",(name,))
        phone = cur.fetchone()[0]
    s = smtplib.SMTP(host='smtp.gmail.com',port=587)
    s.starttls()
    s.login(MY_ADDRESS,PASSWORD)
    msg = MIMEMultipart()
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="New Visitor"
    message = 'You have a Visitor! \n Name : {}\n Email : {}\n Phone : {}\n Time : {}\nDate : {}\n Chat With him ! : {}'.format(name,visem,str(int(phone)),timestart,time_date,chatlink)
    msg.attach(MIMEText(message,'plain'))
    s.send_message(msg)
    del msg