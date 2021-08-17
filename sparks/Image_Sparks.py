import cv2
import image_class
import sparks_analysis
import numpy as np

class Image_Sparks:

    def Image_cropping(self):
        '''Uses numpy type image for selecting and cropping'''
        r = image_class.Image_Processing.select_roi(self)
        imcrop = image_class.Image_Processing.crop_image(self,r)
        return imcrop

    def Image_processing(self):
        '''Uses numpy type image and returns a copy of the image and a filtered image'''
        img_processed, alpha, beta = image_class.Image_Processing.automatic_brightness_and_contrast(self)
        image_class.Image_Processing.display_image(img_processed, 'Image processed',)
        filtered = image_class.Image_Processing.image_filtration (img_processed, 3, 100)
        contours = image_class.Image_Processing.find_contourns(filtered) # Obtains elements by contours
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
        stats_list = []
        for element in contours:
            stats = image_class.Image_Processing.set_threshold(element,1)
            img_mean = image_class.Image_Processing.track_contours (element, img_processed, original, track_number)
            img_row_mean , img_col_mean = image_class.Image_Processing.mean_pixels_intensity (img_mean[4])
            list_img_row.append(img_row_mean)
            list_img_col.append(img_col_mean)
            x_position.append(img_mean [0])
            y_position.append(img_mean [1])
            width.append(img_mean [2])
            high.append(img_mean [3])
            stats_list.append(stats)
            track_number +=1
        return list_img_col, list_img_row, x_position, y_position, width, high,stats_list