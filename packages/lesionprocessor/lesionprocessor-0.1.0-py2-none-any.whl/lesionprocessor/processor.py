import os

from .cmdpattern import commands, receivers, invokers, receivers
from .helpers import constants, utils
from .lesion import ProcessedLesion

def process(input_path:str, unprocessed_dir:str='unprocessed', *, crop_dir:str=None, label_dir:str=None, isolate_dir:str=None, crop_scale:int=1, label_scale:int=1, label_rgb:tuple=(0, 255, 0), contour_limit:int=3, contour_corner_offset:int=5, denoise_kernel_scale:float=10):
    if not os.path.exists(input_path):
        raise Exception('Given input path does not exist.')
    
    out_dirs = [unprocessed_dir, crop_dir, label_dir, isolate_dir]
    out_dirs_to_make = [d for d in out_dirs if d is not None and not os.path.exists(d)]
    if out_dirs_to_make:
        print(f'Following directories do not exist: {out_dirs_to_make}.\nScript will automatically generate them.')
        utils.make_dirs(*out_dirs_to_make)

    cmds = [
        commands.ThresholdCommand(receivers.IsicThresholder()),
        commands.ContourCommand(receivers.IsicContourer(contour_limit, contour_corner_offset)),
        commands.IsolateCommand(receivers.IsicIsolator()),
        commands.CropCommand(receivers.IsicCropper(crop_scale)) if crop_dir else None,
        commands.LabelCommand(receivers.IsicLabeler(label_rgb, label_scale)) if label_dir else None,
        commands.WriteCommand(receivers.IsicImageWriter(unprocessed_dir, crop_dir, label_dir, isolate_dir))
    ]
    cmds = [c for c in cmds if c is not None]

    if os.path.isdir(input_path):
        file_paths = [os.path.join(input_path, p) for p in os.listdir(input_path)]
        img_paths = [f for f in file_paths if f.endswith(constants.SUPPORTED_EXTS)]
        if not img_paths:
            raise Exception('Given input directory does not have any images.')

        initial_data = [ProcessedLesion(file_path=i) for i in img_paths]
    else:
        if not input_path.endswith(constants.SUPPORTED_EXTS):
            raise Exception('Given input file is not an image.')

        initial_data = ProcessedLesion(file_path=input_path)

    invoker = invokers.SuccessiveInvoker(*cmds)
    invoker.execute_commands(initial_data)

    if not os.listdir(unprocessed_dir):
        os.removedirs(unprocessed_dir)

def isolate(input_path:str, out_dir:str, unprocessed_dir:str='unprocessed'):
    process(input_path, unprocessed_dir, isolate_dir=out_dir)

def crop(input_path:str, out_dir:str, unprocessed_dir:str='unprocessed', scale:int=1):
    process(input_path, unprocessed_dir, crop_dir=out_dir, crop_scale=scale)

def label(input_path:str, out_dir:str, unprocessed_dir:str='unprocessed', scale:int=1, rgb:tuple=(0, 255, 0)):
    process(input_path, unprocessed_dir, label_dir=out_dir, label_scale=scale, label_rgb=rgb)
