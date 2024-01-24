from flask import Flask, request, render_template, redirect, url_for,send_file
import mysql.connector
import datetime as dt
import cv2
import numpy as np
import face_recognition
import os
import pandas as pd


# connecting to database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="attendance"  # database named attendance
)
cursor = mydb.cursor()

app = Flask(__name__)

username = ""
password = ""

# First only recognise face and hold the user name
def face():
    global name
    name=""
    path='Students'
    images=[]
    classNames=[]
    myList=os.listdir(path)
    print(path)

    for cls in myList:
        currentImage=cv2.imread(f"{path}/{cls}")
        images.append(currentImage)
        classNames.append(os.path.splitext(cls)[0])#split text and take only first path
    print(classNames)    

    def compute_encodings(images):
        encodeList=[]
        for img in images:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListforKnown=compute_encodings(images)
    print("Encoding Complete")

    cap=cv2.VideoCapture(0)

    for x in range(1):
        success,img=cap.read()
        img_small=cv2.resize(img,(0,0),None,0.25,0.25) #reduce size of web cam captured to speed up the process
        img_small=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        facesCurFrame=face_recognition.face_locations(img_small)
        encodeCurFrame=face_recognition.face_encodings(img_small,facesCurFrame)   



        for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces(encodeListforKnown,encodeFace)
            faceDist=face_recognition.face_distance(encodeListforKnown,encodeFace)
            matchIndex=np.argmin(faceDist)
            
            if matches[matchIndex]:
                name=classNames[matchIndex]
                
    print(name)     


@app.route('/inlocation')
def inlocation():
    returned_value = checkTime()
    print(f"the function returned: {returned_value}")
    return redirect(url_for("status"))


@app.route('/success')
def success():
    return render_template('location.html')

@app.route('/admin')
def admin():
    return '<a href="/download">Download Excel</a>'

@app.route('/download')
def download_excel():
    excel_filename = 'sorted_data.xlsx'  # Replace with your Excel file name
    return send_file(excel_filename, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def form():
    global username, password
    if request.method == 'POST':
        username = request.form['USN']
        password = request.form['Password']
        # Process the user input here
        query = "SELECT * FROM login WHERE usn = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        face()
        print("Detected Face: ")
        print(name)
        if result and (password=="admin"):
            download()
            print("Admin Login Successful!.")
            return render_template ('admin.html')
        elif result and (name==username):
            print("Login successful!")
            print(username)
            return redirect(url_for("success"))
        
    else:
        print("Invalid credentials!")
        # return "Received username: {}, password: {}".format(username, password)

    return render_template('google.html')
# login()

def download():
    # Retrieve data from the database
    query = "SELECT * FROM status"
    cursor.execute(query)
    data = cursor.fetchall()

    # Define column names (adjust these according to your database schema)
    columns = ['USN', 'subject', 'status','date_column', 'time', 'code']

    # Create a DataFrame from the fetched data
    df = pd.DataFrame(data, columns=columns)

    # Convert 'date_column' to datetime format
    df['date_column'] = pd.to_datetime(df['date_column'])

    # Sort the DataFrame by a specific column (e.g., 'column1')
    sorted_df = df.sort_values(by='subject')

    # Close the database connection
   

    # Format 'date_column' as strings in a desired format (e.g., 'YYYY-MM-DD')
    sorted_df['date_column'] = sorted_df['date_column'].dt.strftime('%Y-%m-%d')

    # Store the sorted data in an Excel file
    excel_file_path = 'sorted_data.xlsx'
    sorted_df.to_excel(excel_file_path, index=False)

    print("Data sorted and saved to Excel file:", excel_file_path)
    
@app.route('/status')
def status():
    query1 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    user = username.split()
    subj1 = '21MAI141'
    cursor.execute(query1, (username, subj1))
    data1 = cursor.fetchall()
    query2 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj2 = '21CSE142'
    cursor.execute(query2, (username, subj2))
    data2 = cursor.fetchall()
    query3 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj3 = '21CSE143'
    cursor.execute(query3, (username, subj3))
    data3 = cursor.fetchall()
    query4 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj4 = '21CSE144'
    cursor.execute(query4, (username, subj4))
    data4 = cursor.fetchall()
    query5 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj5 = '21CSE145'
    cursor.execute(query5, (username, subj5))
    data5 = cursor.fetchall()
    query6 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj6 = '21CIP146'
    cursor.execute(query6, (username, subj6))
    data6 = cursor.fetchall()
    query7 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj7 = '21KAN147'
    cursor.execute(query7, (username, subj7))
    data7 = cursor.fetchall()
    query8 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj8 = '21SFT148'
    cursor.execute(query8, (username, subj8))
    data8 = cursor.fetchall()
    query9 = "SELECT * FROM status where usn = (%s) and code=(%s)"
    subj9 = '21CSE149'
    cursor.execute(query9, (username, subj9))
    data9 = cursor.fetchall()

    print("Fetching Attendace Deatils of USN: "+username)

    return render_template('index.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7, data8=data8, data9=data9)


def checkTime():
    current_hour = dt.datetime.now().hour  # current system hour
    current_minute = dt.datetime.now().minute  # current system minute
    current_date = dt.datetime.now()  # current date
    current_day = current_date.weekday()  # current day 0-Monday 6-Sunday
    date1 = dt.datetime.today()
    ddmmyyyyy = dt.date.strftime(date1, "%Y-%m-%d")
    print(ddmmyyyyy)
    print(current_hour, current_minute)
    print(current_date)
    print(current_day)
    # target_hour = 12 #24 hour clock
    # target_minute1 = 0 #lower bound
    # target_minute2 = 5 #upper bound

    s1 = 0
    s2 = 0
    s3 = 0
    # Monday
    if current_day == 0:
        if current_hour == 8 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Database Management Systems", "Present",
                   ddmmyyyyy, "8:30 AM TO 10:30 AM", "21CSE142")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 11 and (current_minute >= 00 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Kannada", "Present", ddmmyyyyy,
                   "11:00 AM TO 12:00 PM", "21KAN147")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 12 and (current_minute >= 00 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Python Programming and Applications",
                   "Present", ddmmyyyyy, "12:00 PM TO 1:00 PM", "21CSE145")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 13 and (current_minute >= 40 and current_minute <= 45):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Statistics, Probability and Graph Theory",
                   "Present", ddmmyyyyy, "1:40 PM TO 2:40 PM", "21MAI141")
            cursor.execute(sql, val)
            mydb.commit()
        else:
            return False

    # Tuesday
    if current_day == 1:
        if current_hour == 8 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Statistics, Probability and Graph Theory",
                   "Present", ddmmyyyyy, "8:30 AM TO 9:30 PM", "21MAI141")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 9 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "MicroControllers and Embedded Systems",
                   "Present", ddmmyyyyy, "9:30 AM TO 10:30 AM", "21CSE142")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 11 and (current_minute >= 00 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Database Management Systems", "Present",
                   ddmmyyyyy, "11:00 AM TO 1:00 PM", "21CSE143")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 13 and (current_minute >= 40 and current_minute <= 45):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Design and Analysis of Algorithms",
                   "Present", ddmmyyyyy, "1:40 PM TO 3:40 PM", "21CSE144")
            cursor.execute(sql, val)
            mydb.commit()
        else:
            return False

    # Wednesday
    if current_day == 2:
        if current_hour == 8 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT INGORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "MicroControllers and Embedded Systems Laboratory",
                   "Present", ddmmyyyyy, "8:30 AM TO 10:30 AM", "21CSE142")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 11 and (current_minute >= 0 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Python Programming and Applications",
                   "Present", ddmmyyyyy, "11:00 AM TO 1:00 PM", "21CSE145")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 13 and (current_minute >= 40 and current_minute <= 45):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Design and Analysis of Algorithms",
                   "Present", ddmmyyyyy, "1:40 PM TO 3:40 PM", "21CSE144")
            cursor.execute(sql, val)
            mydb.commit()
        else:
            return False

    # Thursday
    if current_day == 3:
        if current_hour == 8 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Constituiton of India and Policies ",
                   "Present", ddmmyyyyy, "8:30 AM TO 9:30 AM", "21CIP146")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 9 and (current_minute >= 45 and current_minute <= 50):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Python Programming and Applications",
                   "Present", ddmmyyyyy, "9:30 AM TO 10:30 AM", "21CSE145")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 11 and (current_minute >= 00 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Soft Skills", "Present",
                   ddmmyyyyy, "11:00 AM TO 12:00 PM", "21SFT148")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 12 and (current_minute >= 00 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s)"
            val = (username, "Statistics, Probability and Graph Theory",
                   "Present", ddmmyyyyy, "12:00 PM TO 1:00 PM", "21MAI141")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 13 and (current_minute >= 40 and current_minute <= 45):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s)"
            val = (username, "Bridge Mathematics", "Present",
                   ddmmyyyyy, "1:40 PM TO 3:40 PM")
            cursor.execute(sql, val)
            mydb.commit()
        else:
            return False

    # Friday
    if current_day == 4:
        if current_hour == 8 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "MicroControllers and Embedded Systems",
                   "Present", ddmmyyyyy, "8:30 AM TO 9:30 AM", "21CSE142")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 9 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Statistics, Probability and Graph Theory",
                   "Present", ddmmyyyyy, "9:30 AM TO 10:30 AM", "21MAI141")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 11 and (current_minute >= 00 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Soft Skills", "Present",
                   ddmmyyyyy, "11:00 AM TO 1:00 PM", "21SFT148")
            cursor.execute(sql, val)
            mydb.commit()
        else:
            return False

     # Saturday
    if current_day == 5:
        if current_hour == 8 and (current_minute >= 30 and current_minute <= 35):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Design and Analysis of Algorithms",
                   "Present", ddmmyyyyy, "08:30 AM TO 10:30 AM", "21CSE144")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 11 and (current_minute >= 0 and current_minute <= 5):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Database Management Systems Laboratory",
                   "Present", ddmmyyyyy, "11:00 AM TO 1:00 PM", "21CSE143")
            cursor.execute(sql, val)
            mydb.commit()
        elif current_hour == 13 and (current_minute >= 40 and current_minute <= 45):
            sql = "INSERT IGNORE INTO status (usn,subject,status,date,time,code) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (username, "Internship", "Present",
                   ddmmyyyyy, "1:40 PM TO 3:40 PM", "21CSE149")
            cursor.execute(sql, val)
            mydb.commit()
        else:
            return False


if __name__ == '__main__':
    app.run(debug=True)
cursor.close()
mydb.close()
