from djitellopy import tello
from time import sleep
import cv2

me = tello.Tello()
me.connect()

me.streamon()

while True:
    img=me.get_frame_read().frame
    img=cv2.resize(img,(360,240))
    cv2.imshow("Imagen",img)
    cv2.waitKey(1)
