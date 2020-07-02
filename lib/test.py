from DesktopApp.lib.analysis import dyssynchonia_analysis
from DesktopApp.lib.image import image_data


def analisis_calcio(path, nombre_foto, min_dist_between_maxs, ancho_corte=5):
    image = image_data.get_image_data(path + nombre_foto + ".tif")

    # Select ROI
    fromCenter = False
    showCrosshair = False
    seleted_parameters = cv2.selectROI(image, fromCenter, showCrosshair)

    # Crop image
    x_start = int(seleted_parameters[1])
    x_end = x_start + int(seleted_parameters[3])
    y_start = int(seleted_parameters[0])
    y_end = y_start + int(seleted_parameters[2])

    image = image_data.crop_vertical(image, x_start, x_end)
    image = image_data.crop_horizontal(image, y_start, y_end)

    return dyssynchonia_analysis.analyze_image(image, min_dist_between_maxs, ancho_corte)


if __name__ == '__main__':
    path = '../'
    nombre_foto = 'c3e000'
    x_calibracion = 4.5
    ancho_corte = 5

    analisis_calcio(path, nombre_foto, 20)
