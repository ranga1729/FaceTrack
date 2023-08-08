import cv2
import face_recognition
import pickle
import os

#import student images
folderPath = 'static/images'
pathList = os.listdir(folderPath)

if pathList == []:
    print("No Images were added.")
else: 
    #creating image list and ID list.
    imgList = []
    studentIds = []

    #adding image links and IDs into imgList and studentIds list.
    for path in pathList:
        imgList.append(cv2.imread(os.path.join("static/images/",path)))
        studentIds.append(os.path.splitext(path)[0])

    #print(studentIds)

    #the function for generating encodes of an image and append those data to a list.
    def findEncodings(imageList):
        encodeList = []
        for img in imageList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)

        return encodeList

    print("Encoding started...")

    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]

    #print(encodeListKnown)
    #print(encodeListKnownWithIds[1])

    print("Encoding Completed !")

    #store encoding data and ID list into a pickle file.
    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()

    print("File Saved !")
