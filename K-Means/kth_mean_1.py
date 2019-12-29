import PIL
from PIL import Image
import urllib.request
import io,sys
print(PIL.PILLOW_VERSION)
URL = sys.argv[1] #http://www.w3schools.com/css/trolltunga.jpg
f = io.BytesIO(urllib.request.urlopen(URL).read())
img = Image.open(f)
img = img.show()
img = Image.open(f)
pix = img.load()
for x in range(img.size[0]):
    for y in range(img.size[1]):
        count = 0
        newL = []
        for val in pix[x,y]:
            if val >= 0 and (val<= (255//3)): newL.append(0)
            elif (val >= 255*2//3) and val <= 255: newL.append(255)
            else: newL.append(127)
        pix[x,y] = tuple(newL)
img.show()
