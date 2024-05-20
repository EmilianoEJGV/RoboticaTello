from djitellopy import tello
from time import sleep
##Para añadir delays en algunos comandos

me = tello.Tello()
me.connect()

print(me.get_battery())

me.takeoff()
me.send_rc_control(0,0,0,0)
sleep(2)
me.send_rc_control(0,0,0,0)
me.land()

