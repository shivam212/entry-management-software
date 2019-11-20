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
		name = request.form["user"]
		email = request.form["email"]
		host = request.form["hosts"]
		stuff = "http://127.0.0.1:5000"+url_for("visiturl",visitor=name)
		send_mail1(name,host,stuff,email,time_string)
		send_mail3(name,host)
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
@app.route("/<visitor>",methods=["GET", "POST"])
def visiturl(visitor):
	if request.method == "GET":
		return(render_template("button.html"))
	elif request.method == "POST":
		send_mail2(visitor,"17uec115@lnmiit.ac.in")
		return(render_template("end.html"))
def send_mail1(name,host,stuff,email,timenow):
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart();
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting'
	message = "Hi " + name + ", Your meeting with " + host + " started at " + timenow + ". End your meeting at - " + stuff + " ."
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()		
def send_mail2(name,email):
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart();
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting'
	message = "How was your meeting Mr." + name
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg
	s.quit()
def send_mail3(name,host):
	with sqlite3.connect("first.db") as con:
		cur = con.cursor()
		cur.execute("SELECT email FROM hosts WHERE name=(?)",(host,))
		email = cur.fetchone()[0]
		print(email, file=sys.stderr)
	s = smtplib.SMTP(host='smtp.gmail.com', port=587)
	s.starttls()
	s.login(MY_ADDRESS, PASSWORD)
	msg = MIMEMultipart();
	msg['From']=MY_ADDRESS
	msg['To']=email
	msg['Subject']='Your Meeting'
	message = 'test'
	msg.attach(MIMEText(message,'plain'))
	s.send_message(msg)
	del msg 
# con = sqlite3.connect("first.db")
# curs = con.cursor()
# curs.execute("CREATE TABLE IF NOT EXISTS hosts(id integer PRIMARY KEY, name text, email text, phone real)")
# con.commit()
# curs.execute("INSERT INTO hosts VALUES(1, 'utkarsh','ukulshr',12345)")
# con.commit()
if __name__=="__main__":
	app.run(debug=True)
