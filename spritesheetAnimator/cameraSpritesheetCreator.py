#!/usr/bin/python
import sys
import pygame
import pygame.camera
import pygame.mouse
import os
from glob import glob

pygame.init()
pygame.camera.init()


screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
#hide the mouse
pygame.mouse.set_visible(0)

cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(1440,1080))
cam.start()
cam.set_controls(hflip = True, vflip = True)

def niceShutdown():
    cam.stop()
    pygame.quit()
    sys.exit()

while True:
    screen.fill([0,0,0])
    #drawing code

    image1 = cam.get_image()
    image1 = pygame.transform.scale(image1,(1440,1080))
    screen.blit(image1,(190,0))
        
    pygame.display.update()
         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            niceShutdown()
