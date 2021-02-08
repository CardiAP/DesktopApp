import Image_Sparks
import cv2
import sparks_analysis_prueba
import image_class
import pandas as pd

path = '/media/leandro/Volumen1TB/Lean/Analizador_imagenes_calcio/Sp/Imagenes_confocal/sp_para entrenar/'
photo_name = '3arf005'
image = image_class.Image_Processing(path, photo_name)


image = cv2.imread(image.path + image.photo_name + ".tif")
imcrop = Image_Sparks.Image_Sparks.Image_cropping(image)
contours, img_processed = Image_Sparks.Image_Sparks.Image_processing(imcrop)
list_img_col, list_img_row, x_position, y_position, width, high = Image_Sparks.Image_Sparks.Image_analysis(contours, img_processed, image)
# Detect each event and give it a category
def write_points(event, x_position, y_position, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        img_points.append(flags)
    if event == cv2.EVENT_RBUTTONDOWN:
        img_points.append(flags)
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

df = pd.DataFrame()
for sp in range(0,len(list_img_col)):
    parameters = sparks_analysis_prueba.analysis_process (list_img_col[sp], list_img_row[sp],x_position[sp],y_position[sp],width[sp],high[sp], img_points[sp])
    df = pd.concat([df,parameters])
print(df)
df.to_csv(path + photo_name + 'csv')