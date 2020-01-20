#!/usr/bin/python
import sys
import pygame
import pygame.camera
import pygame.mouse
import os
from glob import glob
from StopMotion import StopMotion

LEFT=0
RIGHT=1
SELECT=2
HOME=3
DELETE=4
PLAY=5
CAPTURE=6

pygame.init()
pygame.camera.init()

# Initialize the joysticks
pygame.joystick.init()
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except:
    joystick=None
    
#load existing projects 
projects=[]
workingDirectory="/home/pi/stopMotionProjects/"
activeDirectories=glob("%s*/" % workingDirectory)
print(activeDirectories)
for directory in activeDirectories:
    print("directory: %s" %directory)
    try:
        project=StopMotion(workingDirectory, directory.split(os.path.sep)[-2])
        projects.append(project)
    except:
        print("trouble loading directory %s" % directory)
        
screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
#hide the mouse
pygame.mouse.set_visible(0)

cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(1440,1080))
cam.start()
cam.set_controls(hflip = True, vflip = True)
frames=[]
thumbnails=[]
mode="home"
project=None
projectIndex=0
projectDimensions=StopMotion.projectDimensions

mask=pygame.Surface(projectDimensions)
#mask=pygame.image.load("simpleMask.png")
#mask = pygame.transform.scale(mask,StopMotion.projectDimensions)
pygame.draw.circle(mask,
                   [255,255,255],
                   (int(projectDimensions[0]/2), int(projectDimensions[1]/2)),
                   int(projectDimensions[1]/2))
addNew=pygame.image.load("add.png")
addNew=pygame.transform.scale(addNew,StopMotion.projectDimensions)
mask.set_colorkey([255,255,255])
spacing=10

def position(index):
    cols=6
    offset=0.5
    if int(index/cols)%2==0:
        offset=0
    return ((projectDimensions[0]+spacing)*(offset+index%cols), spacing+(projectDimensions[1]+spacing)*int(index/cols))

def generateHtml():
    f=open("%sindex.html" % workingDirectory, "w")
    f.write("<html>\n\t<body>\n");
    for project in projects:
        f.write("<div class='project'><img src='%s/thumbnail.jpg'>%s, %d frames</div>" % (project.relativeDirectory, project.relativeDirectory, project.numFrames))
    f.write("</body>\n</html>\n")
    f.close()

def niceShutdown():
    generateHtml()
    cam.stop()
    pygame.quit()
    sys.exit()

while True:
    screen.fill([0,0,0])
    #drawing code
    if mode=="home":
        ind=0
        w,h=pygame.display.get_surface().get_size()
        pygame.draw.circle(screen, [255,255,255], (int(position(projectIndex)[0]+projectDimensions[0]/2), int(position(projectIndex)[1]+projectDimensions[1]/2)), int(projectDimensions[1]/2+spacing))
        for p in projects:
#                pygame.draw.rect(screen,[255,255,255],[offset-10, h/2-10, p.thumbnail.get_width()+20, p.thumbnail.get_height()+20], 0)
            copy=p.thumbnail
            copy.blit(mask,(0,0))
            copy.set_colorkey([0,0,0])
            screen.blit(copy, position(ind))
            ind+=1
        copy=addNew
        copy.blit(mask,(0,255))
        copy.set_colorkey([0,0,0])
        screen.blit(copy, position(len(projects)))        

   
    if mode=="capture":
        image1 = cam.get_image()
        image1 = pygame.transform.scale(image1,(1440,1080))
        screen.blit(image1,(190,0))
        offset=0
        for image in project.thumbnails[-9:]:
            screen.blit(image,(offset,900))
            offset+=image.get_width()+20
      

    if mode=="play":
        if index<len(project.frames):
            screen.blit(project.frames[index], (190,0))
            index+=1
        else:
            mode="capture"
      
    pygame.display.update()
         
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            niceShutdown()
        
        if event.type==pygame.KEYDOWN or event.type==pygame.JOYBUTTONDOWN:
            try:
                key=event.key
            except:
                key=0
            if key ==pygame.K_ESCAPE:
                niceShutdown()
                
            if mode=="home":                
                if key == pygame.K_RIGHT or joystick is not None and joystick.get_button(RIGHT):
                    if projectIndex<len(projects):
                        projectIndex+=1
                        
                elif key == pygame.K_LEFT or joystick is not None and joystick.get_button(LEFT):
                    if projectIndex>0:
                        projectIndex-=1
                            
                elif key==ord(' ') or joystick is not None and joystick.get_button(SELECT):
                    if projectIndex==len(projects):  #make a new project
                        project=StopMotion(workingDirectory)
                        projects.append(project)
                        projectIndex=len(projects)-1
                    else:
                        project=projects[projectIndex]
                        project.loadFrames()
                    mode="capture"
                print(projectIndex)
               
            elif mode=="capture":
                keys = pygame.key.get_pressed() 
                if key==ord('d') or joystick is not None and joystick.get_button(DELETE):
                    project.removeFrame()
                if key==ord(' ') or joystick is not None and joystick.get_button(CAPTURE):
                    project.addFrame(image1)
                if key==ord('p') or joystick is not None and joystick.get_button(PLAY):
                    mode="play"
                    index=0
                if key==ord('h') or joystick is not None and joystick.get_button(HOME):  #back home
                    generateHtml()
                    mode="home"
                    if len(project.frames)==0:
                        projects.remove(project)  #if it's a zombie project, remove it from the master list
                    project.close()
