import cv2
import image_class
import sparks_analysis
import numpy as np

path = '/media/leandro/Volumen1TB/Lean/Analizador_imagenes_calcio/Sp/Imagenes_confocal/sp_para entrenar/'
# path = 'C:/Users/Leand/OneDrive/Documentos/Lean/Analizador_imagenes_calcio/Imagenes_confocal/Rata/C071112/'
photo_name = '2arf001'
image = cv2.imread(path + photo_name + ".tif")    # Read image
image_class.image_processing.__init__(image, image.shape)
r = image_class.image_processing.select_roi(image)  # Select ROI
imcrop = image_class.image_processing.crop_image(image,r)   # Crop ROI
img_processed, alpha, beta = image_class.image_processing.automatic_brightness_and_contrast(imcrop) # Autoprocess brightness and contrast
image_class.image_processing.display_image('crop',img_processed) # Show cropped processed image
filtered = image_class.image_processing.filtration (img_processed, 3, 100) # Filtering
dilate = filtered[0]
original = filtered[1]
cnts = image_class.image_processing.find_contourns(dilate) # Obtain elements by contours

# Iterate thorugh contours and filter for ROI
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

# Detect each event and give it a category
def write_points(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        img_points.append((x, y, flags))
    if event == cv2.EVENT_RBUTTONDOWN:
        img_points.append((x, y, flags))
winname="TAG :: Press ESC to exit; left Click to TAG 1; right Click to TAG 2"
cv2.namedWindow(winname)
img_points = []
cv2.setMouseCallback(winname,write_points)
while True:
    cv2.imshow(winname,img_processed)
    cv2.imshow('original',image)
    if cv2.waitKey(20) & 0xFF ==27:
        break      
cv2.destroyAllWindows()

# Take the processing data to analyze each spark and extract parameters

parameters = sparks_analysis.analysis_process (list_img_col, list_img_row,x,y,width,high,img_points)
print(parameters)
parameters.to_csv()