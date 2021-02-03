import cv2
import numpy as np
from PIL import Image


class Image_Processing:
    
    def __init__(self, path, photo_name):
        self.path = path
        self.photo_name = photo_name
        
    def select_roi (self): 
        ''' This function allows to select a rectangular region of interest. It uses as parameter an image 
        and returns the initial point (x,y) and the width and high of the rectangule.'''
        fromCenter = False  # create the rectangule from de initial point
        showCrosshair = False  # rectangule without a cross in the middle
        roi = cv2.selectROI(self,fromCenter, showCrosshair)
        return roi      

    def crop_image (self,roi):
        '''Crop the image using the ROI positions. This function returns an image.'''
        imCrop = self[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        return imCrop

    def display_image (self, name):
        '''Show image in a window'''
        cv2.imshow(name, self)
        cv2.waitKey(0)  # with 'enter' to break
        cv2.destroyAllWindows()

    def Adjust_brightness_contrast(self, brightness, contrast):
        '''Adjust manually brightness and contrast algebraically. It converts the image to an array
        and returns a filtered image and shows it in a window.'''
        img = np.int16(self)
        img = img * (contrast/128) - contrast + brightness
        img = np.clip(img, 0, 255)
        img = np.uint8(img)
        plt.imshow(img)
        plt.show()
        return img

    def image_rotation (self, degrees):
        '''Rotates an image and returns an image with the same dimensions'''
        imagen = Image.fromarray(self)
        imagen = imagen.rotate(degrees)
        imagen = numpy.array(imagen)

    def image_filtration (self,factor, baseline):
        '''Gaussian filtration using baseline and a proportionality factor. This function returns a filtered image'''
        image_grayscale = cv2.cvtColor(self, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(image_grayscale, (3, 3), 0)
        canny = cv2.Canny(blurred, baseline, factor*baseline, 400)  # edge detection algorithm
        kernel = np.ones((5,5),np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=1)  # it increases the white region in the image or size of foreground object increases
        return dilate

    def find_contourns (self):
        '''Obtain elements of an image returning a list of each individual contour.
        They are Numpy arrays of (x,y) coordinates of boundary points of the object.'''
        countours = cv2.findContours(self, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        countours = countours[0] if len(countours) == 2 else countours[1]
        return countours

    def track_contours (countour, filtered_image, original, track_number):
        '''Calculates up-right position and dimensions of a rectangule image, draws it on the image and tracks it with a number from bottom to top.
        This function returns x_position, y_position, width, high and ROI'''
        x_position,y_position,width,high = cv2.boundingRect(countour)
        cv2.rectangle(filtered_image, (x_position, y_position), (x_position + width, y_position + high), (255,255,0), 2)
        cv2.putText(filtered_image, str(track_number), (x_position-2, y_position - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),2)
        ROI = original[y_position:y_position+high, x_position:x_position+width]
        return x_position, y_position, width, high, ROI
    
    def mean_pixels_intensity (self):
        '''This function uses an image and converts it to an numpy array and calculate the mean value from each line in x and y axis, returning them into two list.'''
        image_array = Image.fromarray(self.astype(np.uint8))
        img_col_mean = np.mean(image_array,axis=0) #list of mean data by columns
        img_row_mean = np.mean(image_array,axis=1) #list of mean data by rows
        img_col_mean = [x.mean() for x in img_col_mean]
        img_row_mean = [x.mean() for x in img_row_mean]
        return img_row_mean , img_col_mean

    def automatic_brightness_and_contrast(self, clip_hist_percent=10):
        '''Return automatic brightness and contrast optimizated image with optional histogram clipping percetage'''
        grayscale_image = cv2.cvtColor(self, cv2.COLOR_BGR2GRAY)

        # Calculate grayscale histogram
        image_histogram = cv2.calcHist([grayscale_image],[0],None,[256],[0,256])
        hist_size = len(image_histogram)

        # Calculate cumulative distribution from the histogram
        cumulative_distribution = []
        cumulative_distribution.append(float(image_histogram[0]))
        for index in range(1, hist_size):
            cumulative_distribution.append(cumulative_distribution[index -1] + float(image_histogram[index]))

        # Locate points to clip
        maximum = cumulative_distribution[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 750

        # Locate left cut
        minimum_gray = 0
        while cumulative_distribution[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size -1
        while cumulative_distribution[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha


        # Calculate new histogram with desired range
        auto_result = cv2.convertScaleAbs(self, alpha=alpha, beta=beta)
        return (auto_result, alpha, beta)