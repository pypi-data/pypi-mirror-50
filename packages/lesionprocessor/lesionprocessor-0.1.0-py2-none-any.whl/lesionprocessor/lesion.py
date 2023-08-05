import os
import numpy as np

from .helpers import constants, utils

class Lesion(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.orig_img = utils.copy_disk_img(file_path, constants.SUPPORTED_EXTS)
        self.img = np.copy(self.orig_img)
        self.filename = os.path.split(file_path)[1]
        self.shape = self.img.shape[:2]

    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        if key == 'orig_img':
            raise Exception('orig_img is read-only')
        return setattr(self, key, value)

class ProcessedLesion(Lesion):
    def __init__(self, **kwargs):
        self.threshold = []
        self.contours = []
        self.cropped = []
        self.labeled = []
        self.isolated = []
        super(ProcessedLesion, self).__init__(**kwargs)