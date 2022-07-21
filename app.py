import string
import time
from tkinter import N
import pyodbc
import os
from flask import Flask, Request, render_template, request, flash

app = Flask(__name__, template_folder="templates")

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbsai.database.windows.net,1433;Database=adb;Uid=sainath;Pwd=Shiro@2018;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()



@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')

@app.route('/ShowNLargest', methods=['GET', 'POST'])
def showDetails():
    cursor = connection.cursor()    
    num1 = request.form.get("num1")
    min_mag = request.form.get("magMin")
   
    max_mag = request.form.get("magMax")

    print("max",max_mag)
    print("min",min_mag)
    param_data = (num1,max_mag,min_mag)
    query_str = "select top "+num1+" a.id, b.place, a.mag from dbo.ds a join dbo.dsi b on a.id = b.id where a.mag <="+max_mag+" and a.mag >="+min_mag 

    print(query_str)
    cursor.execute(query_str+" ORDER BY a.mag DESC")
    N_Laragest_data = cursor.fetchall()
    cursor.execute(query_str+" ORDER BY a.mag ASC")
    N_smallest_data = cursor.fetchall()
    return render_template('ShowNLargest.html',n=num1, data1 = N_Laragest_data, data2 = N_smallest_data)  

@app.route('/Show500KmEarthquakes', methods=['GET', 'POST'])
def show500KmEarthquakes():
    cursor = connection.cursor()   
    degree = (500/111)
    latMax = 32.7355816 + degree
    latMin = 32.7355816- degree
    longMax = -97.1071186 + degree
    longMin = -97.1071186 - degree   
    param_data = (latMax,latMin,longMax,longMin)
    print(" limits are ",param_data)
    cursor.execute("select * from dbo.all_month where latitude <= ? AND latitude >= ? AND longitude <= ? AND longitude >= ?" , param_data)

    data = cursor.fetchall()
    print(len(data))
    return render_template('Show500KmEarthquakes.html', data = data)  


@app.route('/QuakesGreaterThan3', methods=['GET', 'POST'])
def quakesGreaterThan3():
    cursor = connection.cursor()   
    startDate = request.form.get("dateStart")
    endDate = request.form.get("dateEnd")
    print("Start date : ",startDate,"Type is ",type(startDate))
    startDate = startDate.replace("-","/")
    endDate = endDate.replace("-","/")
    print("Start date : ",startDate,"Type is ",type(startDate))
    query_string = "select * from all_month where time >= '"+startDate+"' and time <= '"+endDate+"'  AND mag > 3"
    cursor.execute(query_string)
    data = cursor.fetchall()
    print(len(data))
    return render_template('QuakesGreaterThan3.html', data = data)  


 


if __name__ == '__main__':    
    app.run()

