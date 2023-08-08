from flask import Flask, render_template, request, Response, jsonify, flash, redirect, url_for, session, g
import cv2
import face_recognition
import numpy as np
import pickle
import cvzone
from cs50 import SQL
import os
from datetime import datetime



app = Flask(__name__)

#looking for stored profile pictures in the images folder and generate encodes. 
import EncodeGenerator

#initiating SQL database.
db = SQL("sqlite:///database.db")
print("Database Initialized...")

#user login credentials
users = {"admin" : "admin"}

detectedId = [20230000]

# marked ID list. 
markedIds = []

# getting links to profile pictures in the image folder. 
imgNameWithEXT = os.listdir('static/images')

if imgNameWithEXT == []:
    print("Images were not included.")
else: 
    print("Image folder detected...")
    imgFullLinkList = []
    imgNameList = []

    for path in imgNameWithEXT:
            imgFullLinkList.append(os.path.join("static/images/",path))
            imgNameList.append(os.path.splitext(path)[0])
    print("Images listed.")

#setting the images folder for uploadings using add.html
UPLOAD_FOLDER = 'static/images/'

app.secret_key = "admin"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#setting allowed extensions for uploding new studnet's profile pics.
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



# function for accessing camera using cv2.
# detecting faces using face_recognition
# detecting known face by comparing face encoding data.
def gen_frames(): 
    camera = cv2.VideoCapture(0) 

    #laod the Encode data file
    file = open('EncodeFile.p', 'rb')
    encodeListKnownWithIds = pickle.load(file)
    file.close()
    encodeListKnown  = encodeListKnownWithIds[0]
    studentIds = encodeListKnownWithIds[1]

    while True:
        success, frame = camera.read()

        #add face-recognition function
        imgS = cv2.resize(frame, (0, 0), None, fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        #comprare current face encodes with the pickle file
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("matches", matches)
            print("faceDis", faceDis)
            print(markedIds)
            matchIndex = np.argmin(faceDis)
            matchId = studentIds[matchIndex]

            #print("Match Index", matchIndex)
                
            #to print the rectangle around the detected face.
            #faceDis should be less than 0.4 to be get detected as a known face.
            if matches[matchIndex] and faceDis[matchIndex] < 0.4:
                #print("Known Face Deteted")
                #print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = x1, y1, x2-x1, y2-y1
                cvzone.cornerRect(frame, bbox, rt=0)

                if matchId == detectedId[0]:
                    continue
                else:
                    detectedId.clear()
                    detectedId.append(matchId)
                    #print(detectedId[0])

                #print(matchId)
            else: 
                continue

        # send camera feed to the webapp.
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST','GET'])
def check_login():
    #get form details 

    if request.method == 'POST':
        session.pop('user', None)

        username = request.form.get("username")
        password = request.form.get("password")

        #cross check form inputs with credentials
        if username in users and password == users[username]:
            session['user'] = username
            return render_template("home.html")
        else: 
            #show error message.
            message = "Username or Password is incorrect !"
            return render_template("login.html", message=message)
    
    else: 
        #show error message.
        message = "Username or Password is incorrect !"
        return render_template("login.html", message=message)
    
@app.before_request
def before_request():
    g.user = None
    
    if 'user' in session:
        g.user = session['user']

@app.route('/home')
def home():
    if g.user:
        return render_template("home.html")
    else: 
        #reroute to login
        message = "Please login..."
        return render_template("login.html", message=message)

@app.route('/mark', methods = ['GET'])
def mark_web():
    if g.user:
        return render_template("mark.html")
    
    else: 
        #reroute to login
        message = "Please login..."
        return render_template("login.html", message=message)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/profile_data')
def mark_data(): 
    #if a face detected, data reagarding that face will be obtained from the database. 
    if detectedId[0] != 20230000:
        dataRow = db.execute("SELECT f_name, l_name FROM students WHERE student_id=?", detectedId[0])
        detectedFirstName = dataRow[0]["f_name"]
        detectedLastName = dataRow[0]["l_name"]

    # to get the detected face's profile image.
    if detectedId[0] in imgNameList:
        index = imgNameList.index(detectedId[0])
        link = imgFullLinkList[index]
        #print(link)
    else:
        #print(link)
        #default profile pic.
        link = "/static/css/20230000.png"

    if int(detectedId[0]) == 20230000:
        return jsonify(f_name="Not Detected!", l_name="Not Detected!", Id="Not Detected!", message="Not Detected!", link=link)
    
    elif int(detectedId[0]) not in markedIds:
        markedIds.append(int(detectedId[0]))

        # getting the current date and time
        current_datetime = datetime.now()

        # extract the date
        date = current_datetime.strftime("%Y-%m-%d")
        #print("current date = ", date)

        # extract the time
        time = current_datetime.strftime("%H:%M:%S")
        #print("current time = ", time)

        # execute a sql command to store data of attendance.
        db.execute("INSERT INTO attendance ('student_id','date','time') VALUES (?,?,?)", detectedId[0], date, time)

        #print(date)
        #print(time)
        #sending detected id's profile information to the webapp.
        return jsonify(link=link, f_name=detectedFirstName, l_name=detectedLastName, Id=detectedId[0], message="Marked!")
    
    else:
        return jsonify(link=link, f_name=detectedFirstName, l_name=detectedLastName, Id=detectedId[0], message="Marked!")
       
@app.route('/check')
def check():
    if g.user:
        return render_template("check.html")
    
    else: 
        #reroute to login
        message = "Please login..."
        return render_template("login.html", message=message)

@app.route('/check_date', methods=["POST","GET"])
def check_date():
    if g.user:
        # get the date from the form in check.html
        date = request.form.get("date") 
        #print(date) 
        #calling the database on attendance data. 
        attendance = db.execute("SELECT students.student_id, f_name, l_name, time FROM students JOIN attendance ON students.student_id = attendance.student_id WHERE date=?", date)
        return render_template("check.html", attendance=attendance, date=date)
    
    else: 
        #reroute to login
        message = "Please login..."
        return render_template("login.html", message=message)

@app.route('/add')
def add_html():
    if g.user:
        #setting default id.(can be changed.)
        default_id = int(20230001) 

        #looking for a existing max value.
        max_id = db.execute("SELECT MAX(student_id) AS max_id FROM students;")
        if max_id[0]["max_id"] == None:
            return render_template("add.html", next_id=default_id)
        else:
            #next id is generting by adding 1 to the previous value.
            next_id = int(max_id[0]["max_id"]) +1
            #print(next_id)
            return render_template("add.html", next_id=next_id)
        
    else: 
        #reroute to login
        message = "Please login..."
        return render_template("login.html", message=message)

@app.route('/adding_students', methods=["POST","GET"])
def add_html_form():
    if g.user:
        #getting data from the form of add.html
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        #setting a default id
        default_id = int(20230001)
        #looking for a existing max value.
        max_id = db.execute("SELECT MAX(student_id) AS max_id FROM students;")
        if max_id[0]["max_id"] == None:
            next_id = default_id
        else:
            next_id = int(max_id[0]["max_id"]) +1

        #getting the new student's profile picture.
        file = request.files['file']
        #extracting it's file name with the extension
        file_name = file.filename
        #print(file_name)
        if file and allowed_files(file_name):
            #extractring file's extension.
            extension = file_name.rsplit('.',1)[1]
            #setting the new name for the profile picture.
            new_name = str(next_id) + '.' + extension
            #print(new_name)
            #saving the profile picture in the images folder.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_name))

            #saving a record in the students table
            db.execute("INSERT INTO students ('student_id', 'f_name', 'l_name') VALUES (?,?,?)", next_id, first_name, last_name)
            flash("Image uploaded successfully.")
            return redirect(url_for('add_html'))
        
        else:
            #displaying the error message.
            flash("Allowed image types - PNG, JPG, JPEG.")
            return redirect(url_for('add_html'))
        
    else: 
        #reroute to login
        message = "Please login..."
        return render_template("login.html", message=message)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("login.html")


if __name__ == '__main__':
    app.run()
