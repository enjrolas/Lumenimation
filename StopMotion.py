import datetime
import os
import pygame
from glob import glob
import shutil
from PIL import Image

class StopMotion:
    thumbnailDimensions=(200,150)
    projectDimensions=(400,300)
        
    def __init__(self, workingDirectory, projectDirectory=None):        
        if projectDirectory is None:
            print("making new project")
            self.workingDirectory=workingDirectory
            self.relativeDirectory=datetime.datetime.now().strftime('%B.%-d.%Y %H:%M:%S')
            self.projectDirectory="%s%s" % (self.workingDirectory, self.relativeDirectory)
            print("project directory directory does not exist, creating %s" % self.projectDirectory)
            os.makedirs(self.projectDirectory)
            os.makedirs("%s/frames" % self.projectDirectory)
            self.frames=[]
            self.thumbnails=[]
            self.numFrames=0
        else:
            self.frames=[]
            self.thumbnails=[]
            self.workingDirectory=workingDirectory
            self.relativeDirectory=projectDirectory
            self.projectDirectory="%s%s" % (workingDirectory, projectDirectory)
            print("initializing existing directory %s" % self.projectDirectory)
            tmp=pygame.image.load("%s/thumbnail.jpg" % self.projectDirectory)
            self.numFrames=len(glob("%s/frames/*.jpg" % self.projectDirectory))
            self.thumbnail=pygame.transform.scale(tmp, self.projectDimensions)

    def loadFrames(self):
        num=1
        for frame in sorted(glob("%s/frames/*.jpg" % self.projectDirectory)):
            print("loading: %s %d/%d" % (frame, num, self.numFrames))
            try:
                img=pygame.image.load(frame)
                self.frames.append(img)
                temp=pygame.transform.scale(img, self.thumbnailDimensions)
                self.thumbnails.append(temp)
            except:
                print("problem loading %s" % frame)
            num+=1
        
    def releaseFrames(self):
        self.frames=[]
        self.thumbnails=[]
        
    def generateMovie(self):
        import ffmpeg
        (
            ffmpeg
            .input("%s/frames/%%04d.jpg" % self.projectDirectory, framerate=10)    
            .output("%s/movie.mp4" % self.projectDirectory, **{"crf":21})
            .overwrite_output()
            .run()
        )

    def close(self):
        if len(self.frames)==0:  # delete the project if there are no frames to keep from having zombie projects
            shutil.rmtree(self.projectDirectory)
        else:
#            self.generateMovie()
            self.releaseFrames()
            
    def playMovie(self):
        self.generateMovie()

    def removeFrame(self):
        if len(self.frames)>0:
            self.frames.pop()
            self.numFrames-=1
            self.thumbnails.pop()
            os.remove(sorted(glob("%s/frames/*.jpg" % self.projectDirectory))[-1])  #catch if there are no images left
        
    def addFrame(self,img):
        if len(self.frames)==0:
            pygame.image.save(img, "%s/thumbnail.jpg" % self.projectDirectory)
            temp=pygame.transform.scale(img,self.projectDimensions)            
            self.thumbnail=temp
        self.frames.append(img)
        temp=pygame.transform.scale(img, self.thumbnailDimensions)
        self.thumbnails.append(temp)
        self.numFrames+=1
        pygame.image.save(img, "%s/frames/%04d.jpg" % (self.projectDirectory, len(self.frames)))
