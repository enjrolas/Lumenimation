#!/usr/bin/python
import sys
import pygame
import pygame.camera
import pygame.mouse

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(1440,1080))
cam.start()
cam.set_controls(hflip = True, vflip = True)
