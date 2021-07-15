projectDirectory="/home/pi/stopMotionProjects/December.20.2019 16:23:04/"
def generateMovie():
    import ffmpeg
    (
        ffmpeg
        .input("%s/frames/%%04d.jpg" % projectDirectory, framerate=10)            
        .output("%s/movie.mp4" % projectDirectory, **{"crf":21})
        .overwrite_output()
        .run()
    )

generateMovie()
