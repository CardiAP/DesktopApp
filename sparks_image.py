import cv2
import numpy as np
# import matplotlib.pyplot as plt
from PIL import Image

def select_roi (image):
    fromCenter = False
    showCrosshair = False
    r = cv2.selectROI(image, fromCenter, showCrosshair)
    return r
def crop_image (image, r):
    imCrop = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    return imCrop
def display_image (name , image):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def f(brightness, contrast):
    img = np.int16(imCrop)
    img = img * (contrast/127+1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img = np.uint8(img)
    plt.imshow(img)
    plt.show()
    return img
def rotation (image_path, degrees):
    im = Image.fromarray(image_path)
    im = im.rotate(degrees)
    im = numpy.array(im)
def filtration (image,factor, baseline):
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, baseline, factor*baseline, 400)
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
#     dilate = cv2.dilate(canny, kernel, iterations=1)
    return dilate, original
def find_contourns (image):
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    return cnts
# def plot_histogram (y_data, nombre_foto, label_x, label_y):
#     plt.plot(y_data)
#     plt.title(nombre_foto)
#     plt.xlabel(label_x)
#     plt.ylabel(label_y)
#     plt.show()
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
def image_process (image,path,clip_hist_percent=10):
    if image is None:
        print("Check file path")        
    else:
        r = select_roi (image) # Select ROI
        imCrop = crop_image (image, r)    # Crop image
        display_image ('Image' , imCrop)    # Display cropped image
        
        auto_result, alpha, beta = automatic_brightness_and_contrast(imCrop,clip_hist_percent)
        cv2.imshow('auto_result', auto_result)
        display_image ('Image.png' , imCrop)
        filtered = filtration (auto_result, 2.5, 100)
        dilate = filtered[0]
        original = filtered[1]

        cnts = find_contourns (dilate)    # Find contours

        # Iterate thorugh contours and filter for ROI
        list_img_col = []
        list_img_row = []
        track_number = 0
        x = []
        y = []
        w = []
        h = []
        for c in cnts:
            img_mean = track_contours (c, auto_result, original, track_number)
            img_col_mean = img_mean [0]
            img_row_mean = img_mean [1]
            x.append(img_mean [2])
            y.append(img_mean [3])
            w.append(img_mean [4])
            h.append(img_mean [5])
            track_number +=1
            list_img_col.append (img_col_mean)
            list_img_row.append (img_row_mean)
        display_image ('image' , auto_result)
        return list_img_col, list_img_row,x, y, w, h