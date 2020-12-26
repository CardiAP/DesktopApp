import cv2
import numpy as np
from PIL import Image


class image_processing:
    
    def __init__(self, dimension):
        self.shape = dimension
        
    def select_roi (self):
        fromCenter = False
        showCrosshair = False
        r = cv2.selectROI(self,fromCenter, showCrosshair)
        return r      

    def crop_image (self, r):
        imCrop = self[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        return imCrop

    def display_image (name,self):
        cv2.imshow(name, self)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def f(self, brightness, contrast):
        img = np.int16(self)
        img = img * (contrast/127+1) - contrast + brightness
        img = np.clip(img, 0, 255)
        img = np.uint8(img)
        plt.imshow(img)
        plt.show()
        return img

    def rotation (self, degrees):
        im = Image.fromarray(self)
        im = im.rotate(degrees)
        im = numpy.array(im)

    def filtration (image,factor, baseline):
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        canny = cv2.Canny(blurred, baseline, factor*baseline, 400)
        kernel = np.ones((5,5),np.uint8)
        dilate = cv2.dilate(canny, kernel, iterations=1)
        return dilate, original

    def find_contourns (image):
        cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        return cnts

    def track_contours (c, image, original, track_number):
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,0), 2)
        cv2.putText(image, str(track_number), (x-2, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0),2)
        ROI = original[y:y+h, x:x+w]
        x_data = np.asarray(range(x,x+w),dtype=np.float64)
        #análisis de cada spark
        SI = Image.fromarray(ROI.astype(np.uint8))
        img_col_mean = np.mean(SI,axis=0) #lista de datos del histograma por columna
        img_row_mean = np.mean(SI,axis=1) #lista de datos del histograma por fila
        img_col_mean = [x.mean() for x in img_col_mean]
        img_row_mean = [x.mean() for x in img_row_mean]
        return img_row_mean , img_col_mean, x, y, w, h

    # Automatic brightness and contrast optimization with optional histogram clipping
    def automatic_brightness_and_contrast(image, clip_hist_percent=10):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate grayscale histogram
        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist_size = len(hist)

        # Calculate cumulative distribution from the histogram
        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index -1] + float(hist[index]))

        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 750

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size -1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha


        # Calculate new histogram with desired range and show histogram
        new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
        auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return (auto_result, alpha, beta)