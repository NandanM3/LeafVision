import os           
import sys          #Used to exit the program at certain points
import glob         #Used to find file patterns     
import argparse     #Used for parsing the command line

import cv2
import numpy as np

# --- Loading Image --- #

def load_image(path:str): #returns numpy array
      img = cv2.imread(path)
      if img is None:
            raise FileNotFoundError
      return img

# --- Resizing the image ---        #Ensures the thresholds are compatible and to ensure consistency

def resize_image(img):      #returns numpy array
      width = 600           #standard width we use  
      h,w = img.shape[:2]   #extracts the hight and width only not channel

      ratio = width/w                               #Finds the ratio we'll use to resize
      new_width = int(w*ratio)  
      new_height = int(h*ratio) 
      resized = cv2.resize(img,(new_width,new_height)) #resizes the img
      return resized

# --- Extracting Color Features --- #

def extract_color_features(resized):  #returns hsv image
      hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)  #Convert to HSV to ensure better comparison
      avg_hue = np.mean(hsv[:,:,0])                   #Calculate the average hue    
      avg_saturation = np.mean(hsv[:,:,1])            #Calculate the average saturation
      avg_value = np.mean(hsv[:,:,2])                 #Calculate the average value
      
      return{
            "avg_hue": avg_hue,
            "avg_saturation": avg_saturation,         #Returns all values as a dictionary
            "avg_value": avg_value  
      }

# --- Testing the functions --- #

path = "samples\Tomato_Bacterial_spot_1.jpeg"
img = load_image(path)
resized = resize_image(img)
features = extract_color_features(resized)

cv2.imshow("Resized", resized)
cv2.waitKey(2000)  
cv2.destroyAllWindows()

cv2.imshow("Original", img)
cv2.waitKey(2000)  
cv2.destroyAllWindows()

print("Extracted Color Features:")
for key, value in features.items():
      print(f"{key}: {value}")          




      
      