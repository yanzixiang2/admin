from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'Admin'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('admin-signup.html')




@app.route("/addadmin", methods=['GET', 'POST'])
def AddEmp():
    admin_email = request.form['admin_email']
    admin_password = request.form['admin_password']


    insert_sql = "INSERT INTO Admin VALUES (%s, %s)"
    cursor = db_conn.cursor()


    try:

        cursor.execute(insert_sql, (admin_email, admin_password))
        db_conn.commit()
       

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('login.html')

@app.route("/adminlogin", methods=['GET', 'POST'])
def AdminLogin():
    
    admin_email = request.form['admin_email']
    admin_password = request.form['admin_password']
        
    select_sql = "SELECT * FROM Admin WHERE admin_email = %s AND admin_password = %s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (admin_email, admin_password))
        admin = cursor.fetchone()

        if admin:

                
            return render_template('home.html')  # You can redirect to a dashboard or admin page
        else:
            return render_template('login.html')

    except Exception as e:
        print(f"Error: {e}")
    finally:
            cursor.close()

return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

