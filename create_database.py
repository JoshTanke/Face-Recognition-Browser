import cv2, sys, numpy, os, time, shutil

def makeFace(name):


    haar_file = 'haarcascade_frontalface_default.xml'
    images = 'image_data'      
    path = os.path.join(images, name)

    #creates a new folder for the image data to go
    if not os.path.isdir(path):
        os.mkdir(path)
    (width, height) = (130, 100)    

    #used for detecting user's face
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0) 

    count = 1
    #takes 30 photos of the user
    while count <= 30: 
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        #detects if face is present
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        
        #resizes faces and converts them to grayscale
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            cv2.imwrite('%s/%s.png' % (path,count), face_resize)
        count += 1
        time.sleep(.1)
        #cv2.imshow('OpenCV', im)
        key = cv2.waitKey(10)
        if key == 27:
            break


#deletes a user's image data
def deleteUser(name):
    if len(name) > 1:
        images = 'image_data'      
        path = os.path.join(images, name)
        shutil.rmtree(path, ignore_errors=True)



   




