import pyglet
from pyglet.gl import *
from pyglet.window import key
import cv2
import numpy
import sys

window = pyglet.window.Window()

camera=cv2.VideoCapture(0)

class CustomLoop(pyglet.app.EventLoop):
  def idle(self):    
    dt = self.clock.update_time()
    self.clock.call_scheduled_functions(dt)

    # Redraw all windows
    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_event('on_draw')
        window.flip()
        window._legacy_invalid = False

    # no timout (sleep-time between idle()-calls)
    return 0

def captureImage():
    retval,img = camera.read()
    sy,sx,number_of_channels = img.shape
    number_of_bytes = sy*sx*number_of_channels
    
    img = img.ravel()
    
    image_texture = (GLubyte * number_of_bytes)( *img.astype('uint8') )
    # my webcam happens to produce BGR; you may need 'RGB', 'RGBA', etc. instead
    pImg = pyglet.image.ImageData(sx,sy,'BGR',
                                  image_texture,pitch=sx*number_of_channels)
    print("capturing image")
    return pImg

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        print('Application Exited with Key Press')
        window.close()

@window.event
def on_draw():
    img=captureImage()
    window.clear()    
    img.blit(0,0)

event_loop = CustomLoop()
event_loop.run()
