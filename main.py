import os           
import sys          #Used to exit the program at certain points
import glob         #Used to find file patterns     
import argparse     #Used for parsing the command line

import cv2
import numpy as np

# Loading Image #

def load_image(path:str): #returns numpy array
      img = cv2.imread(path)
      if img is None:
            raise FileNotFoundError
      return img

# Resizing the image #         #Ensures the thresholds are compatible and to ensure consistency

def resize_image(img):      #returns numpy array
      width = 600           #standard width we use  
      h,w = img.shape[:2]   #extracts the hight and width only not channel

      ratio = width/w                               #Finds the ratio we'll use to resize
      new_width = int(w*ratio)  
      new_height = int(h*ratio) 
      resized = cv2.resize(img,(new_width,new_height)) #resizes the img
      return resized




      
      