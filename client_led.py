#Simple example Robot Raconteur client light up M1K led
from RobotRaconteur.Client import *
import time
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

i=0
while True:
	#light up leds 
    m1k_obj.setled(i % 8)
    time.sleep(.5)
    i+=1
