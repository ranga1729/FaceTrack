![FaceTrack Logo](static/logo/logo.png)

# <span style="color:blue">**FACETRACK**</span> - An Attendance Marking System With <span style="color:green">*Face Recognition*</span>

# Video Demo: https://youtu.be/lKf3D25LEwo

# Description:

## Brief :-

> FACETRACK is an attendance marking system which uses Face Recognition technology to identify faces.
FACETRACK is built using programming languages like python(Flask microframework), Javascipts and markup languages like HTML, CSS.

> default login,
> 
>     username : admin
>     password : admin

## Files and their usages :-

## <span style="color:red">**templates and static folders**</span>
As Flask required, all HTML files are inlcuded in the *templates* folder  and all other static files are included in the *static* folder.

* templates folder,
    1. layout.html -basic layout
    1. login.html - admin login page
    1. home.html - homepage/navigation page
    1. mark.html - designed to mark attendance
    1. check.html - designed to retreive and show attandance data from the database.
    1. add.html - designed to add new students. 

<br>

* static folder,
    1. background - contains the backgroung image of all the HTML files.
    1. css - contains all the stylesheets.
    1. images - contains all student images.
    1. javascript - contains all javascript files.
    1. logo - contains the logo of FACETRACK.

<br>

## <span style="color:red">**app.py**</span>

**app.py** is the main application.
you can run it by executing this command in the terminal opened in the same folder as app.py.

    flask run

## <span style="color:red">**database.db**</span>

**database.db** is the on and only database uses in the app.py. It includes two tables,
1. students - stores student details like,
    * student ID
    * First Name
    * Last Name

1. attendance - store attendance details.
    * students ID
    * arrived date
    * arrived time

## <span style="color:red">**EncodeGenerator.py**</span>

EncodeGenerator is another application which created to read all student's images in the **/static/images** folder. It will encode all images and create a list includeing that encode details along with students IDs relevant to each student. Then all of those details will be saved in a **pickle file (EncodeFile.p).**

That pickle file is the source where app.py is getting face encoding details and student IDs at the start of the program.
So It's important to restart the program if you have added new students though **Add** *(add.html)*.


<br>

## **Important points to mention :-**
1. When you adding new students using the **Add(add.html)** app will autogenerate students Id. Id numbers are incrementing by one.
1. When you have added new students using the **Add(add.html)** it won't take immediate effects, You have to restart the application to let **EncodeGenerator.py** to read and encode those new student images.
1. Default student Id is set to **"20230001"**. If you prefer another pattern of Id numbers, change the varibale **default_id** mentioned at the top of the app.py.
Then app will auto increment next Id numbers.
1. Once you run and scanned a face it will store the attendance details. But in a one session you can mark a one face only one time.

<br>

## **Troubleshooting :-**
## 1. **Compiler Errors When Installing Packages** <br>

### **No such file or directory** or 

> Building wheels for collected packages: dlib <br>
  Building wheel for dlib (pyproject.toml) ... error <br>
  error: subprocess-exited-with-error

FACETRACK uses a list of libraries mentioned in the **requirement.txt**. 
Some of those libraries may not install properly due to not having a C Compiler. The root case of theis issue is about a C complier and package mentioned above, not pip.
<br>
(MAC and Linux computers will not face this error but most prabably windows computer will do.) 
<br>
<span style="color:red">**Solution :**</span> <br>
1. Download and install Visual Studio for C++ 
2. Download and install *"tools for cmak"* via https://cmake.org/download/
3. Run this commands in your terminal

    >pip install cmake <br>
    pip install dlib
4. Try again to install those failed packages.
    > pip install face-recognition

<p></p>
<br>

## 2. Black Screen Issue or web cam doesn't show up properly.
If you are using a built in webcam which came with your laptop may be won't work properly with the application or having *Black screen* issues. 

<span style="color:red">**Solution :**</span> <br>
To solve this problem you have to use a seperate web cam.
Then you have to tell the program to use the seperate webcam.

Edit **gen_frames** function at the top of the **app.py** as below. <br>
change the value from 0 to 1 in the **"cv2.VideoCapture(1)"**<br>
(In most of the times 0 means default/built-in webcam.)

    def gen_frames():
        camera = cv2.VideoCapture(0)

    def gen_frames():
        camera = cv2.VideoCapture(1)

(Sometimes your computer may take the separate webcam as 0, in that case you have to keep it as 0 in order to use seperate webcam.)
