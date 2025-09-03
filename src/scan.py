from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import os

def scan_document(image_path, output_dir='saved_images'):

    try:
        # load the image and compute the ratio of the old height
        # to the new height, clone it, and resize it
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image from {image_path}")
            
        ratio = img.shape[0] / 500.0
        orig = img.copy()
        img = imutils.resize(img, height=500)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        # find the contours in the edged image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        screenCnt = None
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4:
                screenCnt = approx
                break

        if screenCnt is None:
           
            h, w = orig.shape[:2]
            screenCnt = np.array([[[0, 0]], [[w, 0]], [[w, h]], [[0, h]]])

        print("Step 2: Find contours of paper")

        # apply the four point transform to obtain a top-down
        # view of the original image
        warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

        # convert the warped image to grayscale, then threshold it
        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset=10, method='gaussian')
        warped = (warped > T).astype('uint8') * 255

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        input_filename = os.path.basename(image_path)
        name, ext = os.path.splitext(input_filename)
        output_path = os.path.join(output_dir, f"{name}_scanned.png")

        # save the scanned image
        cv2.imwrite(output_path, warped)
        print(f"Scanned image saved at: {output_path}")
        
        return output_path
        
    except Exception as e:
        print(f"Error in scan_document: {e}")
        raise e

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help='Path to the image to be scanned')
    args = vars(ap.parse_args())

    try:
        output_path = scan_document(args['image'])
        
        # Load and display images (optional for CLI usage)
        orig = cv2.imread(args['image'])
        warped = cv2.imread(output_path, cv2.IMREAD_GRAYSCALE)
        
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)