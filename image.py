import pyglet
from pyglet.gl import *

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
height, width = 800, 600 # Desired resolution

window = pyglet.window.Window(width, height)
image = pyglet.resource.image('snake.jpg')

image.width = width
image.height = height
image.texture.width = width
image.texture.height = height

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
