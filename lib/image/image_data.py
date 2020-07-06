import cv2
import numpy as np


# Receives a path and name of an image in tif format (the path could be absolute or relative)
# Returns 2d matrix with the intensity of each pixel in each position
# For smoothing we are using a bilateral filter https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#bilateralfilter
def get_image_data(image_name):
    import cv2
    image_matrix = cv2.imread(image_name)
    if image_matrix is None:
        raise ValueError(f'Image {image_name} not found')

    # TODO estos parametros queremos cambiarlos dependiendo de la imagen?
    image_matrix = cv2.bilateralFilter(image_matrix, 20, 300, 300)
    image_matrix = cv2.cvtColor(image_matrix, cv2.COLOR_BGR2GRAY)
    
    return image_matrix 


def crop_vertical(image_matrix, pixel_start, pixel_end):
    return image_matrix[pixel_start:pixel_end]


def crop_horizontal(image_matrix, pixel_start, pixel_end):
    return image_matrix[0:len(image_matrix), pixel_start:pixel_end]


# Receives a 2d Martix and the with of the slice
# Returns a 3d Matrix that has the received matrix splited verticaly by the slice width
# Can raise ValueError if the slice width is bigger than the x axis of the image
# Examples:
# split_vertically_by[[1,2,3,4], [5,6,7,8]], 2) => [[[1,2],[5,6]], [[3,4],[7,8]]]
# split_vertically_by[[1,2,3], [5,6,7]], 2) => [[[1,2],[5,6]], [[3],[7]]]
def split_vertically_by(image_matrix, slice_width):
    import numpy as np
    if slice_width > len(image_matrix[0]): raise ValueError("The value of the slice width needs to be smaller than the len of the x axis")

    image_width = len(image_matrix[0])
    left_over_count = image_width % slice_width
    width_to_split = image_width - left_over_count

    splited_columns = np.asarray(
        [np.asarray(_split_column(column[0:width_to_split], slice_width) + [column[width_to_split:image_width]]) for
         column in image_matrix])
    return np.transpose(splited_columns, (1, 0))

def _split_column(column, slice_width):
    return np.split(column, len(column) / slice_width)
