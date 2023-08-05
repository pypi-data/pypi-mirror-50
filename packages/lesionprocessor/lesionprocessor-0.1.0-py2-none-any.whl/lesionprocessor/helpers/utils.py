import os
import cv2
import numpy as np

from .constants import *

def copy_disk_img(file_path, supported_exts):
    if not os.path.exists(file_path):
        raise Exception('File does not exist')
    if not file_path.endswith(supported_exts):
        raise Exception(f'File is not a supported image type. Supported image types: {SUPPORTED_EXTS}')
    orig_img = cv2.imread(file_path)

    return np.copy(orig_img)

def plot_images(imgs_to_plot, resize_height=None, resize_width=None):
    for id, img in enumerate(imgs_to_plot):
        if resize_width:
            img = resize_image(img, width=resize_width)
        elif resize_height:
            img = resize_image(img, height=resize_height)
        cv2.imshow(str(id), img)
    cv2.waitKey(0)

def make_dirs(*dirs):
    for directory in dirs:
        os.makedirs(directory)