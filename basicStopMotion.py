
from time import sleep
from picamera import PiCamera
from StopMotion import *
import os

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.start_preview()
# Camera warm-up time
sleep(2)


camera.capture('foo.jpg')
