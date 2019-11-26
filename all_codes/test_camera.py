import picamera
import time

picam=picamera.PiCamera()
picam.start_preview()
time.sleep(20)
picam.stop_preview()
picam.close()