import cv2
import image_class
import numpy as np

path = '/media/leandro/Volumen1TB/Lean/Analizador_imagenes_calcio/Sp/Imagenes_confocal/Rata/C071112/'
# path = 'C:/Users/Leand/OneDrive/Documentos/Lean/Analizador_imagenes_calcio/Imagenes_confocal/Rata/C071112/'
photo_name = 'c2ac009'
image = cv2.imread(path + photo_name + ".tif")    # Read image
image_class.image_processing.__init__(image, image.shape)
r = image_class.image_processing.select_roi(image)
imcrop = image_class.image_processing.crop_image(image,r)
img_processed, alpha, beta = image_class.image_processing.automatic_brightness_and_contrast(imcrop)
image_class.image_processing.display_image('crop',img_processed)
filtered = image_class.image_processing.filtration (img_processed, 2.5, 100)
dilate = filtered[0]
original = filtered[1]
cnts = image_class.image_processing.find_contourns(dilate)

# Iterate thorugh contours and filter for ROI
list_img_col = []
list_img_row = []
track_number = 0
x = []
y = []
w = []
h = []
for c in cnts:
    img_mean = image_class.image_processing.track_contours (c, img_processed, original, track_number)
    img_col_mean = img_mean [0]
    img_row_mean = img_mean [1]
    x.append(img_mean [2])
    y.append(img_mean [3])
    w.append(img_mean [4])
    h.append(img_mean [5])
    track_number +=1
    list_img_col.append (img_col_mean)
    list_img_row.append (img_row_mean)
    point = image_class.image_processing.write_points()
    image_class.image_processing.paint_canvas('winname',points)