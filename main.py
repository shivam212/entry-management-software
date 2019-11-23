import sqlite3
import smtplib
import time
import sys
from sqlite3 import Error
from flask import Flask,escape, url_for, request, render_template 
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import gmtime, strftime
MY_ADDRESS = 'spikesensei69@gmail.com'
PASSWORD = 'timepass9'
app = Flask(__name__)
@app.route("/add",methods=["GET","POST"])
def add_host():
	if request.method=="GET":
		return(render_template("add_hosts.html"))
	elif request.method=="POST":
		name = request.form["hostname"]
		phoneno = request.form["phoneno"]
		email = request.form["email"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT into hosts(name,email,phone)values(?,?,?)",
				(name,email,phoneno))
			con.commit()
			# con.close()
		return(render_template("add_hosts2.html"))

@app.route("/",methods=["GET", "POST"])
def input2():
	if request.method == "POST":
		named_tuple = time.localtime() 
		time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		time_date = time.strftime("%m/%d/%Y")
		time_start = time.strftime("%H:%M:%S")
		name = request.form["user"]
		email = request.form["email"]
		host = request.form["hosts"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT into visit(visitor,visitor_email,host,timestart) values(?,?,?,?)",
				(name,email,host,time_start))
			con.commit()
		stuff = "http://127.0.0.1:5000"+url_for("visiturl",visitor=name)
		send_mail1(name,host,stuff,email,time_string)
		send_mail3(name,host,email,time_date,time_start)
		return(render_template("landend.html",user=name,host=host,link_text=stuff,timenow=time_string))
		return redirect(request.url)
	elif request.method == "GET":
		named_tuple = time.localtime() 
		time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
		con = sqlite3.connect("first.db")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM hosts")
		hosts=cur.fetchall()
		return (render_template("my-form.html",hosts=hosts,timenow=time_string))
		
@app.route("/appoint/<visitor>",methods=["GET", "POST"])
def visiturl(visitor):
	if request.method == "GET":
		return(render_template("button.html"))
	elif request.method == "POST":
		named_tuple = time.localtime() 
		time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
		time_date = time.strftime("%m/%d/%Y")
		time_start = time.strftime("%H:%M:%S")
		with sqlite3.connect("first.db") as con:
			cur=con.cursor()
			cur.execute("SELECT * from visit where visitor=(?)",(visitor,))
			details = cur.fetchone()
			cur.execute("DELETE FROM visit WHERE visitor=(?)",(visitor,))
			cur.execute("INSERT INTO totallog(visitor,visitor_email,host,timestart,timeend) values(?,?,?,?,?)",(details[1],details[2],details[3],details[4],time_start))
		send_mail2(visitor)
		return(render_template("end.html",host=details[3],timestart=details[4],timeend=time_start))
def send_mail1(name,host,stuff,email,timenow):
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart();
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting'
	message = "Hi ,\n" + name + "Your meeting with " + host + " started at " + timenow + ". \nEnd your meeting at - " + stuff + " ."
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()		
def send_mail2(name):
	with sqlite3.connect("first.db") as con:
		cur = con.cursor()
		cur2 = con.cursor()
		cur.execute("SELECT host,timestart,timeend FROM totallog WHERE visitor=(?)",(name,))
		answer = cur.fetchone()
		cur2.execute("SELECT email FROM hosts WHERE name=(?)",(answer[0],))
		answer2 = cur2.fetchone()
		print((answer), file=sys.stderr)
		print((answer2), file=sys.stderr)
		# con.commit()
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart();
	msg['From']=MY_ADDRESS
	msg['To']=answer2[0]
	msg['Subject']='Your Meeting with ' + answer[0]
	message = "Details of meeting.\n Name of Visitor : " + name + "\n" + "Check-In Time : " + answer[1] + "\nCheckOut Time : " + answer[2]
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()
def send_mail3(name,host,visem,time_date,timestart):
	with sqlite3.connect("first.db") as con:
		cur = con.cursor()
		cur.execute("SELECT email FROM hosts WHERE name=(?)",(host,))
		email = cur.fetchone()[0]
		# print(email, file=sys.stderr)
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart();
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']="New Visitor"
	message = 'You have a Visitor! \n Name : {}\n Email : {}\n Time : {}\n Date : {}'.format(name,visem,timestart,time_date)
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg 
if __name__=="__main__":
	con = sqlite3.connect("first.db")
	curs = con.cursor()
	curs.execute("CREATE TABLE IF NOT EXISTS hosts(id integer PRIMARY KEY, name text, email text, address text, phone real)")
	curs.execute("CREATE TABLE IF NOT EXISTS totallog(id integer PRIMARY KEY, visitor text, visitor_email text, vistitor_phone real, host text, timestart text, timeend text)")
	curs.execute("CREATE TABLE IF NOT EXISTS visit(id integer PRIMARY KEY, visitor text,visitor_email text, host text, timestart text)")
	con.commit()
	app.run(debug=True)
