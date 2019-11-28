import sqlite3
import time
import os
import sys
from sqlite3 import Error
from flask_wtf.csrf import CSRFProtect
from flask import Flask,escape, url_for, request, render_template, redirect 
from forms import LoginForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from string import Template
from time import gmtime, strftime
from message import send_visitor,send_host_start,send_visitor_2,send_host_start_chat
from txtmsg import send_text_visitor,send_text_host_start,send_text_visitor_2,send_text_host_start_chat
app = Flask(__name__)
csrf = CSRFProtect()
@app.route("/delete",methods=["GET","POST"])
def delete_host():#Function that deletes host from the database.
	if request.method=="GET":#GET method
		con = sqlite3.connect("first.db")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM hosts")
		hosts=cur.fetchall()
		return(render_template("hostdelete.html",hosts=hosts))
	elif request.method=="POST":#POST METHOD
		todel = request.form["hosts"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("DELETE from hosts WHERE name=(?) ",
				(todel,))
			cur.execute("SELECT * FROM hosts")
			hosts=cur.fetchall()
			con.commit()
		return(render_template("hostdelete.html",hosts=hosts))
@app.route("/add",methods=["GET","POST"])
def add_host():#Function that adds host to the databse.
	if request.method=="GET":#GET Method
		return(render_template("add_hosts.html"))
	elif request.method=="POST":#POST Method
		name = request.form["hostname"]
		phoneno = request.form["phoneno"]
		email = request.form["email"]
		address = request.form["Address"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT into hosts(name,email,address,phone)values(?,?,?,?)",
				(name,email,address,phoneno))
			con.commit()
		return(render_template("add_hosts2.html"))
@app.route("/hostdetails",methods=["GET","POST"])
def host_details():#Function to display all host details on the screen,
	if request.method=="GET":
		con = sqlite3.connect("first.db")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM hosts")
		hosts=cur.fetchall()
		return(render_template("hostse.html",hosts=hosts))
	elif request.method=="POST":
		host=request.form["hosts"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * from totallog WHERE host=(?)",
				(host,))
			details=cur.fetchall()
		return(render_template("hostde.html",host=host,details=details))
@app.route("/hostpanel",methods=["GET","POST"])
def host_panel():#Redirects to the host panel.
	return(render_template("hostpage.html"))
@app.route("/",methods=["GET", "POST"])
def home():#The home page redirection.
	form = LoginForm()#Form generated using WTForms
	if request.method == "POST":
		named_tuple = time.localtime() 
		time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
		time_date = time.strftime("%d/%m/%Y")
		time_start = time.strftime("%H:%M:%S")
		if form.validate_on_submit():			
			name = form.name.data
			email = form.email.data
			host = request.form["hosts"]
			phone = form.phone.data
			takeapp = form.submitapp.data
			takechat = form.submitchat.data
		else:
			return redirect(url_for("home"))#Redirecting if the validation fails.
		if takeapp==True:
			with sqlite3.connect("first.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * from visit")
				meet=cur.fetchall()
				cur.execute("SELECT * FROM hosts")
				hosts1=cur.fetchall()
				cur.execute("SELECT host FROM visit")
				busy = cur.fetchall()
				con.commit()
			if (host,) in busy:
				return redirect(url_for("home"))#Redirecting if host is busy,
			with sqlite3.connect("first.db") as con:
				cur = con.cursor()
				cur.execute("INSERT into visit(visitor,visitor_email,visitor_phone,host,timestart) values(?,?,?,?,?)",
					(name,email,phone,host,time_start))
			new=[]
			for hosta in hosts1:
				if (hosta[1],) in busy:
					new.append([hosta[1]+"(Not Available)",hosta[1]])#Checking and editing to show whether host is busy or not,
				else:
					new.append([hosta[1]+"(Available)",hosta[1]])
			if (host,) in busy:
				return (render_template("my-form.html",hosts=new,timenow=time_string))
			else:
				stuff = url_for("visiturl",visitor=name)
				send_visitor(name,host,stuff,email,time_string)
				send_text_visitor(name,host,stuff,phone,time_string)
				send_host_start(name,host,email,time_date,time_start)
				send_text_host_start(name,host,email,time_date,time_start)
				return(render_template("landend.html",user=name,host=host,link_text=stuff,timenow=time_string))#Giving Appointment if not busy.
		elif takechat==True:#For Chat based Appointment
			with sqlite3.connect("first.db") as con:
				cur = con.cursor()
				cur.execute("INSERT into visit(visitor,visitor_email,visitor_phone,host,timestart) values(?,?,?,?,?)",
					(name,email,phone,host,time_start))
				cur.execute("INSERT into messages(sender,message) values(?,?)",(name,"HI!"))
				con.commit()	
			send_host_start_chat(name,host,email,time_date,time_start,"http://127.0.0.1:5000"+(url_for("messaginghost",visitor=name,host=host)))#Notifies Host of chat start
			send_text_host_start_chat(name,host,email,time_date,time_start,"http://127.0.0.1:5000"+(url_for("messaginghost",visitor=name,host=host)))#Notifies Host of chat start
			return(render_template("msgstart.html",link = url_for("messagingvisitor",visitor=name,host=host)))
	elif request.method == "GET":
		named_tuple = time.localtime() 
		time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * FROM hosts")
			hosts=cur.fetchall()
			cur.execute("SELECT host FROM visit")
			busy = cur.fetchall()
		new=[]
		for hosta in hosts:#Checking and Displaying if host is busy.
			if (hosta[1],) in busy:
				new.append([hosta[1]+"(Not Available)",hosta[1]])
			else:
				new.append([hosta[1]+"(Available)",hosta[1]])
		return (render_template("my-form.html",hosts=new,timenow=time_string,form=form))
@app.route("/messagehost/<visitor>/<host>",methods=["GET","POST"])
def messaginghost(visitor,host):#The host side ChatBox
	flag=0
	allmsg=[]
	link = url_for("visiturl",visitor=visitor)
	if request.method=="POST":
		msg=request.form["sendmsg"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO messages(sender,message) values(?,?)",(host,msg))
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			cur.execute("SELECT message from messages WHERE sender=(?)",(visitor,))
			msge = cur.fetchone()
			con.commit()		
		if(allmsg==None):
			flag=1
		if msge==None:#workaround to keep the Host Chat Box and Visitor ChatBox in sync and display this when either side ends the chat.
			return (render_template("last.html"))
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))
	elif request.method=="GET":
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			cur.execute("SELECT message from messages WHERE sender=(?)",(visitor,))
			msge = cur.fetchone()
			con.commit()
		if msge==None:
			return (render_template("last.html"))
		if(allmsg==None):
			flag=1
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))#Displays Messages
@app.route("/messagevisit/<visitor>/<host>",methods=["GET","POST"])
def messagingvisitor(visitor,host):#Visitor Side CheckBox
	flag=0
	allmsg=[]
	if request.method=="POST":
		msg=request.form["sendmsg"]
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO messages(sender,message) values(?,?)",(visitor,msg))
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			cur.execute("SELECT message from messages WHERE sender=(?)",(visitor,))
			msge = cur.fetchone()
		if msge==None:#workaround to keep the Host Chat Box and Visitor ChatBox in sync and display this when either side ends the chat.
			return (render_template("last.html"))
		if(allmsg==None):
			flag=1
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))#Displays messages
	elif request.method=="GET":
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			cur.execute("SELECT message from messages WHERE sender=(?)",(visitor,))
			msge = cur.fetchone()
		if msge==None:
			return (render_template("last.html"))
		if(allmsg==None):
			flag=1
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))
@app.route("/appoint/<visitor>",methods=["GET", "POST"])#Function for ending appointment.
def visiturl(visitor):
	if request.method == "GET":
		with sqlite3.connect("first.db") as con:
			cur=con.cursor()
			cur.execute("SELECT * from visit where visitor=(?)",(visitor,))
			details = cur.fetchone()
		if details==None:
			return("Does not exist")
		return(render_template("button.html"))
	elif request.method == "POST":
		named_tuple = time.localtime() 
		time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
		time_date = time.strftime("%d/%m/%Y")
		time_start = time.strftime("%H:%M:%S")
		with sqlite3.connect("first.db") as con:
			cur=con.cursor()
			cur.execute("SELECT * from visit where visitor=(?)",(visitor,))
			details = cur.fetchone()
			cur.execute("DELETE FROM visit WHERE visitor=(?)",(visitor,))#Deletes from ongoing meeting
			cur.execute("DELETE FROM messages WHERE sender=(?)",(visitor,))#Deletes chat history if messaging is done
			cur.execute("DELETE FROM messages WHERE sender=(?)",(details[4],))#Deletes chat history if messaging is done
			cur.execute("INSERT INTO totallog(visitor,visitor_email,visitor_phone,host,timestart,timeend,dat) values(?,?,?,?,?,?,?)",(details[1],details[2],details[3],details[4],details[5],time_start,time_date))#storing in log of all visitors
		send_visitor_2(visitor,details[2])#sending end mail to visitor
		send_text_visitor_2(visitor)#sending end text to visitor
		return(render_template("end.html",host=details[4],timestart=details[5],timeend=time_start))
if __name__=="__main__":
	SECRET_KEY = os.urandom(32)
	app.config['SECRET_KEY'] = SECRET_KEY
	con = sqlite3.connect("first.db")
	curs = con.cursor()
	### Creation of database and its tables.
	curs.execute("CREATE TABLE IF NOT EXISTS messages(id integer PRIMARY KEY, sender text, message text)")
	curs.execute("CREATE TABLE IF NOT EXISTS hosts(id integer PRIMARY KEY, name text, email text, address text, phone real)")
	curs.execute("CREATE TABLE IF NOT EXISTS totallog(id integer PRIMARY KEY, visitor text, visitor_email text, visitor_phone real, host text, timestart text, timeend text, dat text)")
	curs.execute("CREATE TABLE IF NOT EXISTS visit(id integer PRIMARY KEY, visitor text,visitor_email text,visitor_phone real, host text, timestart text)")
	con.commit()
	app.run(debug=True)
