import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3
import pandas as pd

import warnings

import sqlite3
import random

import smtplib 
from email.message import EmailMessage
from datetime import datetime

warnings.filterwarnings('ignore')



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/about")
def about1():
    return render_template("about.html")


@app.route('/logon')
def logon():
	return render_template('signup-in.html')

@app.route('/login')
def login():
	return render_template('signup-in.html')

@app.route('/home1')
def home1():
	return render_template('home1.html')


@app.route('/home2')
def home2():
	return render_template('home2.html')

@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signup-in.html")


@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signup-in.html")    

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("home1.html")
    else:
        return render_template("signup-in.html")

@app.route("/notebook1")
def notebook1():
    return render_template("DF1.html")

@app.route("/notebook2")
def notebook2():
    return render_template("DF2.html")


@app.route('/predict',methods=['POST'])
def predict():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model_df1.sav')
    predict = model.predict(final4)

    if predict == 0:
        output = "NEGATIVE, PATIENT IS NOT SUFFER FROM HEART DISEASE!" 
    elif predict == 1:
        output = "POSITIVE, PATIENT IS SUFFER FROM HEART DISEASE!"  
    
    
    return render_template('prediction.html', output=output)


@app.route('/predict1',methods=['POST'])
def predict1():
    int_features= [float(x) for x in request.form.values()]
    print(int_features,len(int_features))
    final4=[np.array(int_features)]
    model = joblib.load('model_df2.sav')
    predict = model.predict(final4)

    if predict == 0:
        output = "NEGATIVE, PATIENT IS NOT SUFFER FROM HEART DISEASE!" 
    elif predict == 1:
        output = "POSITIVE, PATIENT IS SUFFER FROM HEART DISEASE!"  
    
    
    return render_template('prediction.html', output=output)



if __name__ == "__main__":
    app.run(debug=False)
