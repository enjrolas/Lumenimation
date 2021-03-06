import io
import picamera
from PIL import image

with picamera.PiCamera() as camera:
    camera.resolution = camera.MAX_IMAGE_RESOLUTION
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    img = Image.open(stream)
    # Crop 10 pixels off the left and right, and 20 off the top and bottom
    cropped = img.crop((10, 20, 10, 20))
    cropped.save('foo.jpg')
