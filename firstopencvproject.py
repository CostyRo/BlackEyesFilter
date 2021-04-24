import dlib
import numpy as np
from cv2 import cv2 as cv
#import all necessary modules

def getRGBValues():

    """Function for getting the RGB values for new eyes"""

    try:
        r=int(input("Enter value for red: "))
        g=int(input("Enter value for green: "))
        b=int(input("Enter value for blue: "))
    except ValueError:
        return (0,0,0)
    #if the values aren't integers return a tuple with zeros

    r=repairValue(r)
    g=repairValue(g)
    b=repairValue(b)
    #if the values are wrong corect them

    return (b,g,r)
    #return a tuple with BGR values

def repairValue(value):

    """Function that repair the values"""

    if value>255:
        return 255
    elif value<0:
        return 0
    else:
        return value
    #if the value is wrong repair him, else return the value

def constructThePath():

    """Function that construct the corect path for a python program"""

    return input("Enter the full path of the image: ").replace("\\","/")
    #replace "\"" with "/"" to be the path corect

def main():

    """Main function of this program"""

    def drawPupils(size):

        """Function that draw the pupils on eyes"""

        cv.circle(result,((leftEyePoints[1][0]+leftEyePoints[2][0])//2,
        (leftEyePoints[1][1]+leftEyePoints[5][1])//2),size,(255,255,255),-1)
        #draw the left pupil

        cv.circle(result,((rightEyePoints[1][0]+rightEyePoints[2][0])//2,
        (rightEyePoints[1][1]+rightEyePoints[5][1])//2),size,(255,255,255),-1)
        #draw the right pupil

    def setSizeForPupils(distance):

        """Function that set the size of the pupils and draw them on eyes"""

        if distance<=20:
            drawPupils(1)
        else:
            drawPupils(2)
        #if the distance is small draw some small pupils,
        #else draw some bigger pupils

    path=constructThePath()
    #set variable path to the path of the image

    image=cv.imread(path)
    #read the image

    if image==None:
        print("Wrong path!!!")
        return
    #if the path is wrong print a error message and destroy the main function

    color=getRGBValues()
    #get the color for eyes

    detector=dlib.get_frontal_face_detector()
    #set the detector for the face

    predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    #set the predictor for the landmark of the face

    grayImage=cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    #transform the image to a gray image

    faces=detector(grayImage)
    #detect the faces

    for face in faces:
        #loop the faces

        landmark=predictor(grayImage,face)
        #set the landmark of the face

        leftEyePoints=[]
        rightEyePoints=[]
        #set the lists for the points of eyes to empty lists

        for i in range(36,42):
            x=landmark.part(i).x
            y=landmark.part(i).y
            leftEyePoints.append([x,y])
        #complete the list with points of the left eye

        for i in range(42,48):
            x=landmark.part(i).x
            y=landmark.part(i).y
            rightEyePoints.append([x,y])
        #complete the list with points of the right eye

        leftEyePoints=np.array(leftEyePoints)
        rightEyePoints=np.array(rightEyePoints)
        #convert the list to numpy arrays

        result=cv.fillPoly(image,[leftEyePoints],color)
        #make the left eye to the given color

        result=cv.fillPoly(result,[rightEyePoints],color)
        #make the right eye to the given color

        setSizeForPupils(leftEyePoints[5][1]-leftEyePoints[1][1])
        #calculate the distance between the top point of the eye and the bottom
        #point of the eye and draw the pupil depending on the distance

        result=cv.bilateralFilter(result,3,75,75)
        #add a blur to the image

        newPhotoName=input("Enter name for the new photo: ")
        #ask for the name of the new image

        cv.imwrite(f"{newPhotoName}.jpg",result)
        #save the new image

while 1:
    #make an infinite loop

    main()
    #make a new image with the filter

    continueOrNot=input("Press Enter to continue the program!")
    #check if the user want to continue to add filter to a new image

    if len(continueOrNot)!=0:
        print("\n")
        break
    #if the user don't want to continue close the program