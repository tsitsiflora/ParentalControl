from PIL import ImageGrab
import time

imageFolderPath = "C:/python27/Screen_captures"
image_list = []
x = 1
while True:
    pic = ImageGrab.grab().save("screen_capture" + str(x) + ".jpg")
    x += 1
    image_list.append(pic)
    time.sleep(6)
    
    
    
