#!/usr/bin/python3

import requests
import sys, getopt
import json
import re
import time
import os
from PIL import Image
from io import BytesIO
from resizeimage import resizeimage

pathPrefix="/workspace/eskimotv/app/"
imgPath=pathPrefix + "img" + time.strftime("/%Y/%m/")
if os.path.isdir(imgPath) == False:
   os.makedirs(imgPath)
   
def saveImage(imgURL,imgName):
   response = requests.get(imgURL)
   img = Image.open(BytesIO(response.content))
   new_height = int(img.height * (max_width / img.width))
   img = img.resize((max_width,new_height))
   img = resizeimage.resize_crop(img,[1920,900])
   img.save(imgPath + imgName,optimize=True,quality=60)
   return imgSuffix + imgName

def slugify(s):
    s = s.lower()
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')
    return s
    
def main(argv):
#Get options from command line.
    try:
        opts, args = getopt.getopt(argv,"i:t:",["image=","title="])
    except getopt.GetoptError:
        print('Usage: img -i "image url" -t "image title')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-i','--image'):
            imgURL = arg
        elif opt in ('-t','--title'):
            title = arg
        else:
            print('Usage: img -i "image url" -t "Image Title')
            sys.exit(2)
         
    try:
        imgName=slugify(title) + ".jpg"
        imgURL
    except:
        print('Usage: python3 img.py -i "image url" -t "Image Title"')
        sys.exit(2)
         
    saveImage(imgURL,imgName)
    print('<img class="img-responsive article-pic" src="{{ "/img%s" | prepend: site.cdnurl }}" alt="%s" title="%s">' % (time.strftime("/%Y/%m/") + imgName,title,title))
    
    
if __name__ == "__main__":
   main(sys.argv[1:])