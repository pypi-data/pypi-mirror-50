import os
import cv2
import numpy as np

from ..lesion import ProcessedLesion
from ..helpers import constants, utils

def has_contour(lesion):
    contours = lesion['contours']
    return len(contours) > 0

class IsicThresholder:
    def threshold(self, lesion):
        gray = cv2.cvtColor(lesion['img'], cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, 
            thresh=0, 
            maxval=255, 
            type=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        lesion['threshold'] = th
        lesion['img'] = th
        return lesion

class IsicDenoiser:
    def __init__(self, kernel_scale=1):
        self._kernel_scale = kernel_scale

    def _approx_kernel(self, width):
        kernel = int(width * 0.01 * self._kernel_scale)
        kernel -= kernel % 2
        kernel += 1
        return (kernel, kernel)

    def denoise(self, lesion:ProcessedLesion):
        _, img_width = lesion['shape']
        kernel = self._approx_kernel(img_width)

        opening = cv2.morphologyEx(lesion['img'], 
            op=cv2.MORPH_OPEN, 
            kernel=np.ones(kernel, np.uint8))
        closing = cv2.morphologyEx(opening, 
            op=cv2.MORPH_CLOSE, 
            kernel=np.ones(kernel, np.uint8))

        lesion['img'] = closing
        return lesion

class IsicContourer:
    def __init__(self, limit=3, corner_offset=10):
        self._limit = limit
        self._corner_offset = corner_offset

    def _filter_larger_contours(self, contours, limit):
        return sorted(contours, key=cv2.contourArea, reverse=True)[:limit]

    def _remove_corners(self, contours, img_width, img_height, corner_offset):
        def _touches_corner(contour):
            x, y, w, h = cv2.boundingRect(contour)

            x_min = corner_offset
            x_max = img_width - corner_offset
            y_min = corner_offset
            y_max = img_height - corner_offset

            touches_lt = x <= x_min and y <= y_min
            touches_lb = x <= x_min and y+h >= y_max
            touches_rt = x+w >= x_max and y <= y_min
            touches_rb = x+w >= x_max and y+h >= y_max
            return touches_lt or touches_lb or touches_rt or touches_rb
        
        return [c for c in contours if not _touches_corner(c)]

    def contour(self, lesion):
        img_height, img_width = lesion['shape']

        contours, _ = cv2.findContours(lesion['img'],
            mode=cv2.RETR_TREE, 
            method=cv2.CHAIN_APPROX_SIMPLE)
        larger_contours = self._filter_larger_contours(contours, self._limit)
        target_contours = self._remove_corners(larger_contours, 
            img_width, img_height, self._corner_offset)

        lesion['contours'] = target_contours

        return lesion

class IsicCropper:
    def __init__(self, scale=1):
        self._scale = scale

    def _get_rect_pts(self, contour):
        x1, y1, w, h = cv2.boundingRect(contour)
        x2 = x1 + w
        y2 = y1 + h
        return x1, y1, x2, y2

    def crop(self, lesion):
        if not has_contour(lesion):
            return lesion

        img_copy = np.copy(lesion['orig_img'])
        img_height, img_width = lesion['shape']
        padding_coeff = 0.08 * self._scale
        padding = int(padding_coeff * img_width)
        contours = lesion['contours']

        brpts = map(self._get_rect_pts, contours)
        xs, ys, xs2, ys2 = zip(*brpts)
        x_start = min(xs)
        y_start = min(ys)
        x_end = max(xs2)
        y_end = max(ys2)

        x_start_padded = max(x_start - padding, 0)
        y_start_padded = max(y_start - padding, 0)
        x_end_padded = min(x_end + padding, img_width)
        y_end_padded = min(y_end + padding, img_height)

        cropped = img_copy[y_start_padded:y_end_padded, x_start_padded:x_end_padded]

        lesion['cropped'] = cropped
        return lesion

class IsicLabeler:
    def __init__(self, rgb=(0, 255, 0), scale=1):
        self._rgb = rgb
        self._scale = scale

    def _get_thickness(self, width):
        thickness = (width * 3)/1500 * self._scale
        return int(thickness)

    def label(self, lesion):
        if not has_contour(lesion):
            return lesion

        contours = lesion['contours']
        img_copy = np.copy(lesion['orig_img'])
        _, width = lesion['shape']
        cv2.drawContours(img_copy, contours, -1, self._rgb, self._get_thickness(width))
        lesion['labeled'] = img_copy
        
        return lesion

class IsicIsolator:
    def __init__(self, scale=1):
        self._scale = scale

    def isolate(self, lesion):
        img_copy = np.copy(lesion['orig_img'])
        height, width = lesion['shape']
        threshold = lesion['threshold']
        contours = lesion['contours']

        mask = np.zeros(lesion['shape'], np.uint8)
        cv2.drawContours(mask, contours, -1, (255,255,255), cv2.FILLED)
        isolated = cv2.bitwise_or(img_copy, img_copy, mask=mask)

        lesion['isolated'] = isolated
        return lesion

class IsicImageWriter:
    def __init__(self, unprocessed_dir='unprocessed', crop_dir=None, label_dir=None, isolate_dir=None):
        self._crop_dir = crop_dir
        self._label_dir = label_dir
        self._isolate_dir = isolate_dir
        self._unprocessed_dir = unprocessed_dir

    def write(self, lesion):
        columns_to_write = {
            constants.CROP_COL: self._crop_dir,
            constants.LABEL_COL: self._label_dir,
            constants.ISOLATE_COL: self._isolate_dir,
        }
        columns_to_write = {k:v for k,v in columns_to_write.items() if v is not None}

        for col, dirpath in columns_to_write.items():
            if len(lesion[col]) == 0:
                out_path = os.path.join(self._unprocessed_dir, lesion['filename'])
                cv2.imwrite(out_path, lesion['orig_img'])
                return
            out_path = os.path.join(dirpath, lesion['filename'])
            cv2.imwrite(out_path, lesion[col])
