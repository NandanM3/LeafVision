# LeafVision

## Video Demo  
<https://youtu.be/v8Xc5ps4uYo> 

## Description

LeafVision is a command-line Python program that analyzes images of tomato leaves to determine plant health and identify common nutrient deficiencies using color-based image processing. The program focuses on visual indicators such as changes in leaf color and applies rule-based logic to classify the plant as healthy, nitrogen deficient, potassium deficient, or unclear.

This project was built as a final project for CS50 and is designed to demonstrate practical applications of image processing, feature extraction, and structured program design without relying on machine learning.

---

## Background

Nutrient deficiencies and plant stress often cause visible changes in leaf color, such as yellowing or browning. While these symptoms are commonly identified through visual inspection, they can be difficult to assess consistently due to lighting conditions, background noise, and subjective human judgment.

LeafVision explores whether basic computer vision techniques can assist in identifying these changes more objectively. The project relies on deterministic image processing and manually defined thresholds.

---

## How the Program Works

The program follows a structured pipeline to analyze a leaf image:

### Image Input and Resizing  
An image file path is provided via the command line using `argparse`. The image is loaded with OpenCV and resized to a fixed width of 600 pixels while preserving its aspect ratio. Standardizing image dimensions ensures consistency when extracting color features.

### Leaf Masking  
The resized image is converted from BGR to HSV color space. A green color mask is applied to isolate the leaf region and reduce background interference. This step significantly improves accuracy by ensuring that only leaf pixels contribute to feature calculations.

### Feature Extraction  
From the masked image, the average Hue, Saturation, and Value (HSV) values are calculated. These values represent the overall color characteristics of the leaf and serve as the primary features used for classification.

### Healthy Baseline Comparison  
A healthy baseline is created by averaging HSV values from multiple healthy tomato leaf images. The extracted features from the test image are compared against this baseline to measure deviation from a healthy leaf.

### Rule-Based Classification  
Based on the calculated differences, predefined thresholds are applied to classify the leaf as:
- Healthy  
- Nitrogen Deficient  
- Potassium Deficient  
- Anomaly (uncertain classification)

These thresholds were determined through manual testing and refinement.

---
## Testing and Debugging

Testing was performed using multiple healthy and deficient tomato leaf images sourced from agricultural visual guides. Each classification threshold was adjusted based on observed HSV differences printed by the program. Debugging focused on identifying overlap between deficiencies and refining rules to minimize misclassification.

Edge cases where the output did not clearly match a known deficiency are intentionally labeled as anomalies rather than forcing an incorrect classification.

---


## Design Choices and Evolution

Several design decisions evolved over the course of development. Initially, the program analyzed the entire image without masking, which led to inconsistent results due to background interference. This limitation motivated the introduction of HSV-based masking.

The decision to avoid machine learning was intentional. While ML models could potentially achieve higher accuracy, they would require larger datasets. For a CS50 final project, I believed a rule-based approach better demonstrates understanding of algorithms, data processing, and program structure.

The project is modular by design, with separate functions for image loading, resizing, masking, feature extraction, comparison, and classification. This structure allows for easy debuuging and expansion.

---

## Usage

Run the program from the command line:

```bash
python main.py --image <path_to_image>
```
## Expected Output 
The program outputs the:
 - Hue Difference
 - Saturation Differecne
 - Value Difference 
 - The classification result 

## Technologies Used

- **Python 3**  
  Python was used as the main programming language for this project because it is easy to read, easy to debug, and very well suited for experimentation. The ecosystem of libraries made it possible to implement computer vision techniques, numerical calculations, and command-line tools efficiently within a single project.

- **OpenCV (cv2)**  
  OpenCV was used for all image processing tasks in this project. It handled operations such as reading images from disk, resizing them, converting between color spaces, and  applying masksUsing. 

- **NumPy**  
  NumPy was used to perform numerical operations on image data. Since images are represented as multi-dimensional arrays, NumPy made it easy to compute average Hue, Saturation, and Value values across the leaf region. It also allowed for fast and clean mathematical operations, which were essential for calculating feature differences and applying rule-based thresholds during classification.

- **argparse**  
  Argparse was used to handle command-line arguments and make the program interactive. It allows the user to provide an image path when running the program, which makes LeafVision flexible and easy to test with different inputs.



## Limitations and Future Improvements

The program is currently calibrated specifically for tomato leaves, and the classification thresholds may not generalize well to other plant species. The program also relies on fixed thresholds, making it sensitive to poor lighting conditions or low-quality images.

Future improvements could include expanding the dataset, supporting additional nutrient deficiencies, and exploring adaptive or learning-based approaches while maintaining interpretability.

## AI use

AI was mainly used to answer some of the "how to" questions and for debugging assistance. All core design decisions, threshold selection, program structure, and implementation were completed independently.









