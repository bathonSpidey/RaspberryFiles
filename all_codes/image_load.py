from PIL import Image

img=Image.open('download.jpeg')
print(img.format, img.size)