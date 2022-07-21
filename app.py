import string
import time
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
    num1 = int(request.form.get("num1"))    
    cursor.execute("select top {} * from dbo.all_month ORDER BY MAG DESC".format(num1))
    data = cursor.fetchall()
    return render_template('ShowNLargest.html', data = data)  

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

