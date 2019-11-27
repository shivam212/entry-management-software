import sqlite3
import time
import sys
from sqlite3 import Error
from flask import Flask,escape, url_for, request, render_template 
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from string import Template
from time import gmtime, strftime
from message import send_visitor,send_host_start,send_visitor_2
from txtmsg import send_text_visitor,send_text_host_start,send_text_visitor_2
app = Flask(__name__)
@app.route("/delete",methods=["GET","POST"])
def delete_host():
	if request.method=="GET":
		con = sqlite3.connect("first.db")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("SELECT * FROM hosts")
		hosts=cur.fetchall()
		return(render_template("hostdelete.html",hosts=hosts))
	elif request.method=="POST":
		todel = request.form["hosts"]
		print(todel, file=sys.stderr)
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("DELETE from hosts WHERE name=(?) ",
				(todel,))
			cur.execute("SELECT * FROM hosts")
			hosts=cur.fetchall()
			con.commit()
		return(render_template("hostdelete.html",hosts=hosts))
@app.route("/add",methods=["GET","POST"])
def add_host():
	if request.method=="GET":
		return(render_template("add_hosts.html"))
	elif request.method=="POST":
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
def host_details():
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
		print(details, file=sys.stderr)
		return(render_template("hostde.html",host=host,details=details))
@app.route("/hostpanel",methods=["GET","POST"])
def host_panel():
	return(render_template("hostpage.html"))
@app.route("/",methods=["GET", "POST"])
def home():
	if request.method == "POST":
		named_tuple = time.localtime() 
		time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
		time_date = time.strftime("%d/%m/%Y")
		time_start = time.strftime("%H:%M:%S")
		name = request.form["user"]
		email = request.form["email"]
		host = request.form["hosts"]
		phone = request.form["phone"]
		print(host,file=sys.stderr)
		if request.form["submit-button"]=="Take Appointment":
			with sqlite3.connect("first.db") as con:
				cur = con.cursor()
				cur.execute("SELECT * from visit")
				meet=cur.fetchall()
				cur.execute("SELECT * FROM hosts")
				hosts1=cur.fetchall()
				cur.execute("SELECT host FROM visit")
				busy = cur.fetchall()
				con.commit()
			with sqlite3.connect("first.db") as con:
				cur = con.cursor()
				cur.execute("INSERT into visit(visitor,visitor_email,host,timestart) values(?,?,?,?)",
					(name,email,host,time_start))
			new=[]
			for hosta in hosts1:
				if (hosta[1],) in busy:
					new.append([hosta[1]+"(Not Available)",hosta[1]])
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
				return(render_template("landend.html",user=name,host=host,link_text=stuff,timenow=time_string))
		elif request.form["submit-button"]=="Take Remote Appointment(Chat)":
			with sqlite3.connect("first.db") as con:
				cur = con.cursor()
				cur.execute("INSERT into visit(visitor,visitor_email,host,timestart) values(?,?,?,?)",
					(name,email,host,time_start))
				con.commit()	
			print(url_for("messaginghost",visitor=name,host=host))
			print(name,host)
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
			print(busy,hosts,file=sys.stderr)
		new=[]
		for hosta in hosts:
			if (hosta[1],) in busy:
				new.append([hosta[1]+"(Not Available)",hosta[1]])
			else:
				new.append([hosta[1]+"(Available)",hosta[1]])
		print(new)
		return (render_template("my-form.html",hosts=new,timenow=time_string))
@app.route("/messagehost/<visitor>/<host>",methods=["GET","POST"])
def messaginghost(visitor,host):
	flag=0
	allmsg=[]
	link = url_for("visiturl",visitor=visitor)
	if request.method=="POST":
		msg=request.form["sendmsg"]
		print(msg,file=sys.stderr)
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO messages(sender,message) values(?,?)",(host,msg))
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			cur.execute("SELECT message from messages WHERE sender=(?)",(visitor,))
			msge = cur.fetchall()
			con.commit()		
		if(allmsg==None):
			flag=1
		print("hi",msge,file=sys.stderr)
		if ('hasended',) in msge:
			return ("meeting ended")
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))
	elif request.method=="GET":
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			cur.execute("SELECT message from messages WHERE sender=(?)",(visitor,))
			msge = cur.fetchall()
			con.commit()
		print(msge,file=sys.stderr)
		if ('hasended',) in msge:
			return ("meeting ended")
		if(allmsg==None):
			flag=1
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))
@app.route("/messagevisit/<visitor>/<host>",methods=["GET","POST"])
def messagingvisitor(visitor,host):
	flag=0
	allmsg=[]
	if request.method=="POST":
		msg=request.form["sendmsg"]
		print(msg,file=sys.stderr)
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO messages(sender,message) values(?,?)",(visitor,msg))
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			con.commit()
		print("host=",host,"visitor=",visitor,file=sys.stderr)
		if(allmsg==None):
			flag=1
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))
	elif request.method=="GET":
		print("host=",host,"visitor=",visitor,file=sys.stderr)
		with sqlite3.connect("first.db") as con:
			cur = con.cursor()
			cur.execute("SELECT * from messages")
			allmsg=cur.fetchall()
			con.commit()
		print(allmsg,file=sys.stderr)
		if(allmsg==None):
			flag=1
		return	(render_template("msg.html",flag=flag,allmsg=allmsg,name=visitor))
@app.route("/appoint/<visitor>",methods=["GET", "POST"])
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
			cur.execute("DELETE FROM visit WHERE visitor=(?)",(visitor,))
			cur.execute("DELETE FROM messages WHERE sender=(?)",(visitor,))
			cur.execute("DELETE FROM messages WHERE sender=(?)",(details[3],))
			cur.execute("DELETE FROM messages WHERE sender=(?)",(details[3],))
			cur.execute("INSERT INTO messages(sender,message) values(?,?)",(visitor,"hasended"))
			cur.execute("INSERT INTO totallog(visitor,visitor_email,host,timestart,timeend,dat) values(?,?,?,?,?,?)",(details[1],details[2],details[3],details[4],time_start,time_date))
		send_visitor_2(visitor,details[2])
		send_text_visitor_2(visitor)
		return(render_template("end.html",host=details[3],timestart=details[4],timeend=time_start))
if __name__=="__main__":
	con = sqlite3.connect("first.db")
	curs = con.cursor()
	curs.execute("CREATE TABLE IF NOT EXISTS messages(id integer PRIMARY KEY, sender text, message text)")
	curs.execute("CREATE TABLE IF NOT EXISTS hosts(id integer PRIMARY KEY, name text, email text, address text, phone real)")
	curs.execute("CREATE TABLE IF NOT EXISTS totallog(id integer PRIMARY KEY, visitor text, visitor_email text, vistitor_phone real, host text, timestart text, timeend text, dat text)")
	curs.execute("CREATE TABLE IF NOT EXISTS visit(id integer PRIMARY KEY, visitor text,visitor_email text, host text, timestart text)")
	con.commit()
	app.run(debug=True)
