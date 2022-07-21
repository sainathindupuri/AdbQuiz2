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

@app.route('/Question13', methods=['GET', 'POST'])
def ZTime():
    cursor = connection.cursor()   
    time1 = request.form.get("time1")
    time2 = request.form.get("time2")

    query_str = "SELECT top 1 b.net,count(a.id) from dbo.ds a join dbo.dsi b on a.id = b.id where DATEPART(HOUR, a.time) >="+time1+" AND DATEPART(HOUR, a.time) <="+time2+" group by b.net order by count(a.id) "
    cursor.execute(query_str)
    smallest = cursor.fetchall()
    query_str = query_str +" desc"
    print(query_str)
    cursor.execute(query_str)
    largest = cursor.fetchall()
    return render_template('Question13.html', data1 = smallest, data2=largest)  


 


@app.route('/Question11', methods=['GET', 'POST'])
def Question11():
    cursor = connection.cursor()    
    net = request.form.get("net")
    min_mag = request.form.get("magMin")   
    max_mag = request.form.get("magMax")
    newMag = request.form.get("newMag")

    query_str = "UPDATE  dbo.ds SET mag ="+newMag+" where id in (SELECT a.id from dbo.ds a join dbo.dsi b on a.id = b.id where b.net = '"+net+"' ) and mag <=" +max_mag+" and mag>="+min_mag 
    cursor.execute(query_str)
    rows_effected = cursor.rowcount
    cursor.commit()
    print("rows ",rows_effected)
    return render_template('Question11.html', rows_count = rows_effected, net = net)  


@app.route('/searachquakebylat', methods=['GET', 'POST'])
def searachquakebylat():
    lat1 = request.form.get("lat1")
    lat2 = request.form.get("lat2")
    long1 = request.form.get("long1")
    long2 = request.form.get("long2")
    print("Incoming dates : ", lat1, lat2)
    cursor.execute("select * from ds inner join dsi on ds.id = dsi.id where latitude between '{}' and '{}' and longitude between '{}' and '{}' ;".format(lat1,lat2,long1,long2))
    result = cursor.fetchall()
    return render_template('searachquakebylat.html', list1= result)


if __name__ == '__main__':    
    app.run()

