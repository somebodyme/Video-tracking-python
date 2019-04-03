import numpy as np
import cv2
import time

film = cv2.VideoCapture("C:/Users/grego/OneDrive/Documents/FMF/Projektno delo/20.3. video Projektno delo/1.AVI")

lower_z = np.array([40,50,50])
upper_z = np.array([80,255,255])

lower_r = np.array([168,100,100])
upper_r = np.array([175,255,255])

output = open("C:/Users/grego/OneDrive/Documents/FMF/Projektno delo/izvoz.txt","w+")
a = 1
video_length = int(film.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
print ("Number of frames: ", video_length)
while True:
    ret, buffer = film.read()
    if buffer is None:
        break
    frame = cv2.cvtColor(buffer, cv2.COLOR_BGR2HSV)
   #zelena

    mask_z = cv2.inRange(frame, lower_z, upper_z)
    coord_z = cv2.findNonZero(mask_z)

    povprecje_z = np.median(coord_z, axis=0)



   #rdeča

    mask_r = cv2.inRange(frame, lower_r,upper_r)

    #prikaz=cv2.bitwise_and(frame,frame,mask=mask_r)
    #cv2.imshow("t",prikaz)
    #cv2.waitKey(0)

    coord_r = cv2.findNonZero(mask_r)
    povprecje_r = np.median(coord_r,axis=0)

    output.write(str(a))
    output.write(np.array2string(povprecje_r)+","+np.array2string(povprecje_r))
    output.write("\n")
    a = a+1


output.close()
film.release()