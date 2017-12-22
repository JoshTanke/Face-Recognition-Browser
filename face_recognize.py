import cv2, sys, numpy, os, time
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
image_data = 'image_data'

def checkFace():
    #Create a list of images and a list of corresponding names
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(image_data):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(image_data, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
    (width, height) = (130, 100)

    if id == 0:
        return None
    #Create a Numpy array from the two lists above
    (images, lables) = [numpy.array(lis) for lis in [images, lables]]

    #OpenCV trains a model from the images
    model = cv2.face.FisherFaceRecognizer_create()
    model.train(images, lables)

    #Use fisherRecognizer on camera stream to compare current user to image data
    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0)
    count = 1
    while count <= 20:
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            prediction = model.predict(face_resize)
            print(prediction)
            if prediction[1]<500:
                return names[prediction[0]]
        count += 1
        time.sleep(.1)    
        
    return None


#alternative function for adding user (see create_database for other)
def addUser(name):

    haar_file = 'haarcascade_frontalface_default.xml'
    images = 'image_data'      
    path = os.path.join(images, name)

    if not os.path.isdir(path):
        os.mkdir(path)
    (width, height) = (130, 100)    

    face_cascade = cv2.CascadeClassifier(haar_file)
    webcam = cv2.VideoCapture(0) 

    count = 1
    while count <= 30: 
        (_, im) = webcam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
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

        
        


