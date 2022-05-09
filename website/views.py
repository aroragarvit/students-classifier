from flask import Flask,Blueprint,render_template,request,flash,redirect,session,url_for,send_file   # Just like a normal flask application, a blueprint defines a collection of views, templates and static assets.
import pandas as pd 
import pickle
import numpy as np
from csv import writer 
         

views=Blueprint('views',__name__)  # now register this blue print in crate app 

@views.route('/home',methods=["GET","POST"])
def home():
     if 'loggedin' in session:
        model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
        if request.method=="POST":
            uid = request.form.get("Roll-no")
            Name = request.form["name"]
            raisedhands = int(request.form['raise'])
            VisITedResources = int(request.form['visited'])
            AnnouncementsView = int(request.form['announce'])
            Discussion = int(request.form['discuss'])
            absent = request.form['absent']
            satisfy = request.form['satisfy']

            df = pd.read_csv("D:\Project onkaar\project_modified\website\static\students.csv")

            if uid in df["UID"].values:
                flash("WARNING -------  UID already exist in database",category="error")
                
                return render_template("home.html")
            
            else:

                satisfy_text=satisfy
                absent_text=absent

                if absent == "Under-7":
                    absent = 1
                elif absent == "Above-7":
                    absent = 0
    
                if satisfy == "Good":
                    satisfy = 1
                elif satisfy == "Bad":
                    satisfy = 0
    
                a = np.array([raisedhands, VisITedResources,
                             AnnouncementsView, Discussion, satisfy, absent])
                a = np.reshape(a, (-1, 6))
                
                result = model.predict(a)
    
                if result == 0:
                    result = "H"
                elif result == 1:
                    result = "L"
                elif result == 2:
                    result = "M"
                
                row = [uid, Name,raisedhands, VisITedResources,
                         AnnouncementsView, Discussion, satisfy_text , absent_text ,result]
                print(row)

                with open("D:\Project onkaar\project_modified\website\static\students.csv", 'a',newline="") as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(row)
                    f_object.close()
    
                return render_template("result.html", value=result , name=Name , uid=uid)

        return render_template("home.html")
     else:
        return redirect(url_for('auth.login'))

@views.route("/download")
def download_file():
    path="D:\Project onkaar\project_modified\website\static\students.csv"
    return send_file(path,as_attachment=True)