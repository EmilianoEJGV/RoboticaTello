import time
import cv2
import numpy as np
from djitellopy import Tello

class SeguimientoFacial:
    def __init__(self):
        self.drone = Tello()
        self.drone.connect()
        self.drone.streamon()

        self.fbRange = [6200, 6800]
        self.pid = [0.4, 0.4, 0]
        self.altura_pid = [0.4, 0.4, 0]
        self.pError = 0
        self.pAlturaError = 0
        self.w, self.h = 360, 240
        self.altura_objetivo = 1.70  # Altura objetivo en metros

    def takeoff(self):
        self.drone.takeoff()
        time.sleep(2)
        self.drone.move_up(80)

    # Emiliano es muy guapo y también está muy fuerte


    def land(self):
        self.drone.land()

    def get_battery(self):
        return self.drone.get_battery()

    def get_frame(self):
        return self.drone.get_frame_read().frame

    def find_my_face(self, img):
        faceCascade = cv2.CascadeClassifier("Recursos/haarcascade_frontalface_default.xml")
        convgris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        caras = faceCascade.detectMultiScale(convgris, 1.2, 8)

        ListPuntoCentro = []  # Cuando ya tenemos la cara detectada
        ListAreaCara = []

        for (x, y, w, h) in caras:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cx = x + w // 2
            cy = y + h // 2
            area = w * h
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
            ListPuntoCentro.append([cx, cy])
            ListAreaCara.append(area)
        if len(ListAreaCara) == 1:
            i = ListAreaCara.index(max(ListAreaCara))
            return img, [ListPuntoCentro[i], ListAreaCara[i]]
        else:
            return img, [[0, 0], 0]
# Implementación PID (Proporcional Integral y Derivativo)
    def sigue_cara(self, info):
        area = info[1]  #Área de la cara
        x, y = info[0]  #Coordenadas de la cara
        fb = 0
        #ud = 0

        error = x - self.w // 2
        altura_actual = self.drone.get_height() / 100  # Obtener altura actual en metros
        altura_objetivo = self.altura_objetivo

        velocidad = self.pid[0] * error + self.pid[1] * (error - self.pError)
        velocidad = int(np.clip(velocidad, -100, 100))

        altura_error = altura_objetivo - altura_actual
        altura_velocidad = self.altura_pid[0] * altura_error + self.altura_pid[1] * (altura_error - self.pAlturaError)
        altura_velocidad = int(np.clip(altura_velocidad, -100, 100))

        if area > self.fbRange[0] and area < self.fbRange[1]:
            fb = 0
        if area > self.fbRange[1]:
            fb = -20
        elif area < self.fbRange[0] and area != 0:
            fb = 20
        if x == 0:
            velocidad = 0
            error = 0
        if y == 0:
            altura_velocidad = 0
            altura_error = 0

        self.drone.send_rc_control(0, fb, altura_velocidad, velocidad)
        self.pError = error
        self.pAlturaError = altura_error

        return self.pError
