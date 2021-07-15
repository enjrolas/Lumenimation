import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution=(2592, 1944)
    camera.zoom=(0.2, 0.2, 0.6, 0.6)
    camera.start_preview()
    while True:
        pass

