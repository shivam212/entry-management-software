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
	message = "Hi," + name + "Your meeting with " + host + " started at " + timenow + ".\nEnd your meeting at - " + stuff + " ."
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
	message = "Details of meeting.\n Name of Visitor : " + name + "\n" + "Check-In Time : " + answer[1] + "\nCheckOut Time : " + answer[2] +"\nAddress :"+answer2[0]+"\nPhone"+str(int(answer2[1]))
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