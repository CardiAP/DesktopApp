import cv2
import image_class
import sparks_analysis
import numpy as np

def Read_image(path, photo_name):
    '''Reads an image using path and the file name as numpy.ndarray'''
    image = cv2.imread(path + photo_name + ".tif")
    return image

def Image_cropping(image):
    '''Uses numpy type image for selecting and cropping'''
    image_class.image_processing.__init__(image, image.shape)
    r = image_class.image_processing.select_roi(image)
    imcrop = image_class.image_processing.crop_image(image,r)
    return imcrop

def Image_processing(image):
    '''Uses numpy type image and returns a copy of the image and a filtered image'''
    img_processed, alpha, beta = image_class.image_processing.automatic_brightness_and_contrast(image)
    image_class.image_processing.display_image('Image processed',img_processed)
    filtered = image_class.image_processing.image_filtration (img_processed, 3, 100)
    contours = image_class.image_processing.find_contourns(filtered) # Obtains elements by contours
    return contours, img_processed

def Image_analysis(contours, img_processed, original):
    '''Iterates through contours and filter for ROI, and returns the dimension of elements contours 
    and converts narray to list of averages'''
    list_img_col = []
    list_img_row = []
    track_number = 0
    x_position = []
    y_position = []
    width = []
    high = []
    for element in contours:
        img_mean = image_class.image_processing.track_contours (element, img_processed, original, track_number)
        img_row_mean , img_col_mean = image_class.image_processing.mean_pixels_intensity (img_mean[4])
        list_img_row.append(img_row_mean)
        list_img_col.append(img_col_mean)
        x_position.append(img_mean [0])
        y_position.append(img_mean [1])
        width.append(img_mean [2])
        high.append(img_mean [3])
        track_number +=1
    return list_img_col, list_img_row, x_position, y_position, width, high