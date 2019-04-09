import numpy as np
import cv2
import math

#lokacia videa
film = cv2.VideoCapture("C:/Users/grego/OneDrive/Documents/FMF/Projektno delo/CIMG2826.AVI")

#array za koordinate
rdeca = np.empty((0,2), float)
zelena = np.empty((0,2), float)
povprecje_r = np.empty((0,2), float)
povprecje_z = np.empty((0,2), float)
# meje za barve
lower_z = np.array([40,50,50])
upper_z = np.array([80,255,255])
lower_r = np.array([170,110,110])
upper_r = np.array([175,255,255])

# txt file za output
output = open("C:/Users/grego/OneDrive/Documents/FMF/Projektno delo/izvoz.txt","w+")
a = 1
#informacija o dolžini videa
video_length = int(film.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
print ("Number of frames: ", video_length)

#ANALIZA VIDEA
while True:
    ret, buffer = film.read()
    if buffer is None:
        break

    #pretvorba barvnega prostora
    frame = cv2.cvtColor(buffer, cv2.COLOR_BGR2HSV)

   #detekcija zelene pike
    mask_z = cv2.inRange(frame, lower_z, upper_z)
    coord_z = cv2.findNonZero(mask_z)
    if coord_z is not None:
        povprecje_z = np.median(coord_z, axis=0)

   #detekcija rdeče pike
    mask_r = cv2.inRange(frame, lower_r,upper_r)
    coord_r = cv2.findNonZero(mask_r)
    if coord_r is not None:
        povprecje_r = np.median(coord_r, axis=0)

    #prikaz=cv2.bitwise_and(frame,frame,mask=mask_r)
    #cv2.imshow("t",prikaz)
    #cv2.waitKey(0)

    #zapis koordinat v txt in array
    output.write(str(a))
    output.write(np.array2string(povprecje_r)+","+np.array2string(povprecje_z))
    output.write("\n")
    a = a+1
    zelena = np.append(zelena, povprecje_z, axis=0)
    rdeca = np.append(rdeca,povprecje_r, axis=0)


output.close()
film.release()

#ANALIZA PODATKOV

# cm/px, t/frame
gostota_pik=1.0
spf = 1.0/120

#HITROST RDEČE
arr = np.amin(rdeca,axis=0)
b = np.argwhere(rdeca==arr[1])
frame_odboja = b[0,0]+1


dx_pred = rdeca[frame_odboja,0]-rdeca[0,0]
dy_pred = rdeca[frame_odboja,1]-rdeca[0,1]

v_pred = (dx_pred**2+dy_pred**2)**0.5*gostota_pik/(frame_odboja*spf)
smer_pred = np.arctan(dy_pred/dx_pred)*180/np.pi


dx_po = rdeca[-1,0]-rdeca[frame_odboja,0]
dy_po = rdeca[-1,1]-rdeca[frame_odboja,1]

v_po = (dx_po**2+dy_po**2)**0.5*gostota_pik/((video_length-frame_odboja)*spf)
smer_po = np.arctan(dy_po/dx_po)*180/np.pi


#KOTNA HITROST ZELENE
y = 1
vsota_kotov_pred=0
kot_n = np.arctan((zelena[0,1]-rdeca[0,1])/(zelena[0,0]-rdeca[0,0]))
while y <= frame_odboja :
    kot_n1 = np.arctan((zelena[y,1]-rdeca[y,1])/(zelena[y,0]-rdeca[y,0]))
    vsota_kotov_pred += np.abs(np.abs(kot_n1)-np.abs(kot_n))
    kot_n = kot_n1
    y +=1

vsota_kotov_po = 0

while y < video_length :
    kot_n1 = np.arctan((zelena[y, 1] - rdeca[y, 1]) / (zelena[y, 0] - rdeca[y, 0]))
    vsota_kotov_po += np.abs(np.abs(kot_n1) - np.abs(kot_n))
    kot_n = kot_n1
    y += 1

kotna_hitrost_pred = vsota_kotov_pred/(frame_odboja*spf)
kotna_hitrost_po = vsota_kotov_po/((video_length-frame_odboja)*spf)

print(v_pred,smer_pred,kotna_hitrost_pred,"\n", v_po,smer_po,kotna_hitrost_po)