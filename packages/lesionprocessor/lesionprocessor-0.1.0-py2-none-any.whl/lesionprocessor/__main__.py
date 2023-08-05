import argparse
import cv2

from .processor import crop, label, isolate
from .helpers import utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    parser.add_argument('--type',
        required=True,
        nargs='?',
        choices=['crop', 'label', 'isolate'])
        
    parsed, _ = parser.parse_known_args()

    if parsed.type == 'crop':
        crop(parsed.input, parsed.output)
    elif parsed.type == 'label':
        label(parsed.input, parsed.output)
    elif parsed.type == 'isolate':
        isolate(parsed.input, parsed.output)
