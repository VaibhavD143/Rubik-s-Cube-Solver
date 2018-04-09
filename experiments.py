from image_processing import *
import numpy as np
import cv2
from color_resolver import *

im = cv2.imread("front.jpg")

rimg = RubiksImage(im,0,"side",False)

rimg.analyze_file(im)

print(rimg.data)

colors = rimg.data

ind = 0
for i in colors:
	h,s,v = rgb2hsv(colors[i][0],colors[i][1],colors[i][2])
	print(ind,(colors[i][0],colors[i][1],colors[i][2]),(h,s,v),resolve_color(h,s,v))