import prueba_image_spark

# path = '/media/leandro/Volumen1TB/Lean/Analizador_imagenes_calcio/Sp/Imagenes_confocal/sp_para entrenar/'
path = 'C:/Users/Leand/OneDrive/Documentos/Lean/Analizador_imagenes_calcio/Imagenes_confocal/Rata/C071112/'
photo_name = '2arf001'

image = prueba_image_spark.Read_image(path, photo_name)
imcrop = prueba_image_spark.Image_cropping(image)
contours = prueba_image_spark.Image_processing(imcrop)
img_processed = prueba_image_spark.Image_processing(contours)
original = prueba_image_spark.Image_processing(img_processed)
img_data = prueba_image_spark.Image_analysis(contours, img_processed, original)

list_img_col = img_data[0]
list_img_row = img_data[1]
x_position = img_data[2]
y_position = img_data[3]
width = img_data[4]
high = img_data[5]
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

parameters = sparks_analysis.analysis_process (list_img_col, list_img_row,x,y,width,high,img_points)
print(parameters)
#parameters.to_csv()