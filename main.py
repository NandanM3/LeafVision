import os           
import sys          #Used to exit the program at certain points   
import argparse     #Used for parsing the command line

import cv2
import numpy as np

# --- Loading Image --- 

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

# --- Extracting Color Features --- 
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

# --- Creating Mask ---

def create_leaf_mask(img):

      #using a green mask to remove background pixels and isolate the leaf region
      #This is will remove noise and increase accuracy
      
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

      lower_green = np.array([20, 40, 20])   #lower bound for green in HSV
      upper_green = np.array([120, 255, 255]) #upper bound for green in HSV

      mask = cv2.inRange(hsv, lower_green, upper_green)  #creates the mask
      mask = cv2.medianBlur(mask, 5)                            #applies a blur to remove some noise

      masked_img = cv2.bitwise_and(img, img, mask=mask)  #applies the mask to the image 

      return masked_img

# --- Healthy Thresholds --- 

def healthy_thresholds():     #returns dict     

      #Calculates average color features for healthy images

      healthy_img1 = load_image("samples/Tomato_Healthy_1.jpeg")
      healthy_img2 = load_image("samples/Tomato_Healthy_2.jpeg")
      healthy_img3 = load_image("samples/Tomato_Healthy_3.jpeg")

      healthy_resized1 = resize_image(healthy_img1)
      healthy_resized2 = resize_image(healthy_img2)   
      healthy_resized3 = resize_image(healthy_img3)
      
      healthy_masked1 = create_leaf_mask(healthy_resized1)
      healthy_masked2 = create_leaf_mask(healthy_resized2)
      healthy_masked3 = create_leaf_mask(healthy_resized3)

      healthy_features1 = extract_color_features(healthy_masked1)
      healthy_features2 = extract_color_features(healthy_masked2)
      healthy_features3 = extract_color_features(healthy_masked3)

      avg_healthy_features = {
            "avg_hue": (healthy_features1["avg_hue"] + healthy_features2["avg_hue"] + healthy_features3["avg_hue"]) / 3,
            "avg_saturation":(healthy_features1["avg_saturation"] + healthy_features2["avg_saturation"] + healthy_features3["avg_saturation"]) / 3,
            "avg_value": (healthy_features1["avg_value"] + healthy_features2["avg_value"] + healthy_features3["avg_value"]) / 3
      }

      return avg_healthy_features


# --- Comparing Features ---       

def compare_features(healthy, test):   #returns dict 
      #calculates the difference between healthy and test images
      return{
            "hue_diff": healthy["avg_hue"] - test["avg_hue"],                       
            "saturation_diff": healthy["avg_saturation"] - test["avg_saturation"],  
            "value_diff": healthy["avg_value"] - test["avg_value"]
      }


# --- Classifying Features ---  
def classification(differences):

      hue_diff = differences["hue_diff"]
      saturation_diff = differences["saturation_diff"]
      value_diff = differences["value_diff"]

      # Healthy
      # Very small differences in all channels
      if abs(hue_diff) < 6 and abs(saturation_diff) < 10 and abs(value_diff) < 5: #abs() used to get positive values                  
            return "The plant appears to be healthy."

      # Nitrogen Deficiency
      # Pale yellow leaves → VERY low saturation & value, hue strongly negative
      if saturation_diff < -40 and value_diff < -40 and hue_diff < -25:
            return "The plant may have Nitrogen Deficiency (Pale yellow leaves detected)."

      # Pottassium Deficiency
      # Brown edges → low saturation, value moderately low, hue only mildly negative
      if saturation_diff < -40 and value_diff < -10 and hue_diff >= -25:
            return "The plant may have Potassium Deficiency."

      # Anomaly
      return "The plant condition is unclear, further analysis may be required (anomaly)."


      

# --- Parsing Command Line Arguments --- 
def parse_arguments():      #Used to parse command line arguments(extract file path for the image user wants to test)
      parser = argparse.ArgumentParser(description="Plant Disease Detection based on Color Features")

      parser.add_argument(
            "--image",
            type=str,
            help="Path to the image to be tested",
            required=True
      )
      args = parser.parse_args()    #parses the arguments
      if not args.image:
            parser.error("No action requested, add --image")  #if no arguments provided, show error

      return args


# --- Main --- 
def main():
      path = parse_arguments().image
      try:
            test_img = load_image(path)
      except FileNotFoundError:
            print("Error: Image not found at path",path)
            sys.exit(1)
      test_resized = resize_image(test_img)
      test_masked = create_leaf_mask(test_resized)
      test_features = extract_color_features(test_masked)
      healthy_features = healthy_thresholds()
      differences = compare_features(healthy_features, test_features)

      print("Hue Difference:", differences["hue_diff"])
      print("Saturation Difference:", differences["saturation_diff"])
      print("Value Difference:", differences["value_diff"])
      
      result = classification(differences)
      
      print(result)

     
if __name__ == "__main__":
      main()





      
      