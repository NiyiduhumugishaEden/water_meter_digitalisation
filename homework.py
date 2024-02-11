import cv2
import pytesseract
import numpy as np

# Function to preprocess the image
def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast in case it is too low
    contrast = cv2.normalize(gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    
    # Apply thresholding to binarize the image
    # Using adaptive thresholding instead of global threshold (OTSU)
    thresh = cv2.adaptiveThreshold(contrast, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
    
    return thresh

# Function to extract text from the image using Tesseract
def extract_text(image_path, output_path):
    # Read the image from the path
    image = cv2.imread(image_path)

    # Check if image is loaded correctly
    if image is None:
        print(f"Error: Image at {image_path} not found.")
        return

    # Preprocess the image for OCR
    preprocessed_image = preprocess_image(image)

    # Specify the path to tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Use Tesseract to extract text
    # Adding more configurations like 'digits' to focus on digit recognition
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
    
    # Debug: Show the preprocessed image
    # Remove this in production
    cv2.imshow('Preprocessed image', preprocessed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Debug: Print OCR result to console
    print("OCR result:", text)
    
    # Save the extracted text to a .txt file
    with open(output_path, 'w') as file:
        file.write(text)

# Path to the image file
image_path = r'C:\Users\IT MODERN\Documents\python\water meter digitalized\water.png'  # Replace with your image path

# Path to save the .txt file
output_path = r'C:\Users\IT MODERN\Documents\python\water meter digitalized\extracted_text.txt'  # Replace with your output path

# Perform text extraction and save to .txt
extract_text(image_path, output_path)
