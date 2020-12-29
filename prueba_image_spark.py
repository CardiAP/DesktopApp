import cv2
import image_class
import sparks_analysis
import numpy as np

def read_image(path, photo_name):
    image = cv2.imread(path + photo_name + ".tif")    # Read image
    return image

def Crop(image):
    image_class.image_processing.__init__(image, image.shape)
    r = image_class.image_processing.select_roi(image)  # Select ROI
    imcrop = image_class.image_processing.crop_image(image,r)   # Crop ROI
    return imcrop

def process(image):
    img_processed, alpha, beta = image_class.image_processing.automatic_brightness_and_contrast(image) # Autoprocess brightness and contrast
    image_class.image_processing.display_image('crop',img_processed) # Show cropped processed image
    filtered = image_class.image_processing.filtration (img_processed, 3, 100) # Filtering
    dilate = filtered[0]
    original = filtered[1]
    cnts = image_class.image_processing.find_contourns(dilate) # Obtain elements by contours
    return cnts, img_processed, original

# Iterate thorugh contours and filter for ROI
def analysis(cnts, img_processed, original):
    list_img_col = []
    list_img_row = []
    track_number = 0
    x = []
    y = []
    width = []
    high = []
    for c in cnts:
        img_mean = image_class.image_processing.track_contours (c, img_processed, original, track_number)
        img_col_mean = img_mean [0]
        img_row_mean = img_mean [1]
        x.append(img_mean [2])
        y.append(img_mean [3])
        width.append(img_mean [4])
        high.append(img_mean [5])
        track_number +=1
        list_img_col.append (img_col_mean)
        list_img_row.append (img_row_mean)
    return list_img_col, list_img_row, x, y, width, high