import numpy as np
import os
from loguru import logger
import cv2
import typing
from findit import FindIt

from stagesepx import toolbox


class BaseHook(object):
    def __init__(self, *_, **__):
        # default: dict
        logger.debug(f'start initialing: {self.__class__.__name__} ...')
        self.result = dict()

    def do(self, frame_id: int, frame: np.ndarray, *_, **__):
        logger.debug(f'hook: {self.__class__.__name__}, frame id: {frame_id}')


class ExampleHook(BaseHook):
    def __init__(self):
        # you can handle result by yourself
        # change the type, or anything you want
        super().__init__()
        self.result = dict()

    def do(self, frame_id: int, frame: np.ndarray, *_, **__):
        super().do(frame_id, frame, *_, **__)
        frame = toolbox.turn_grey(frame)
        self.result[frame_id] = frame.shape


class FrameSaveHook(BaseHook):
    """ add this hook, and save all the frames you want to specific dir """

    def __init__(self, target_dir: str, compress_rate: float = None, *_, **__):
        super().__init__(*_, **__)

        # init target dir
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

        # compress rate
        self.compress_rate = compress_rate or 0.2

        logger.debug(f'target dir: {target_dir}')
        logger.debug(f'compress rate: {compress_rate}')

    def do(self,
           frame_id: int,
           frame: np.ndarray,
           *_, **__):
        super().do(frame_id, frame, *_, **__)
        compressed = toolbox.compress_frame(frame, compress_rate=self.compress_rate)
        target_path = os.path.join(self.target_dir, f'{frame_id}.png')
        cv2.imwrite(target_path, compressed)
        logger.debug(f'frame saved to {target_path}')


class InvalidFrameDetectHook(BaseHook):
    def __init__(self,
                 compress_rate: float = None,
                 black_threshold: float = None,
                 white_threshold: float = None,
                 *_, **__):
        super().__init__(*_, **__)

        # compress rate
        self.compress_rate = compress_rate or 0.2

        # threshold
        self.black_threshold = black_threshold or 0.95
        self.white_threshold = white_threshold or 0.9

        logger.debug(f'compress rate: {compress_rate}')
        logger.debug(f'black threshold: {black_threshold}')
        logger.debug(f'white threshold: {white_threshold}')

    def do(self,
           frame_id: int,
           frame: np.ndarray,
           *_, **__):
        super().do(frame_id, frame, *_, **__)
        compressed = toolbox.compress_frame(frame, compress_rate=self.compress_rate)
        black = np.zeros([*compressed.shape, 3], np.uint8)
        white = black + 255
        black_ssim = toolbox.compare_ssim(black, compressed)
        white_ssim = toolbox.compare_ssim(white, compressed)
        logger.debug(f'black: {black_ssim}; white: {white_ssim}')

        self.result[frame_id] = {
            'black': black_ssim,
            'white': white_ssim,
        }


class TemplateCompareHook(BaseHook):
    def __init__(self,
                 template_dict: typing.Dict[str, str],
                 *args, **kwargs):
        """
        args and kwargs will be sent to findit.__init__

        :param template_dict:
            # k: template name
            # v: template picture path
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fi = FindIt(*args, **kwargs)
        self.template_dict = template_dict

    def do(self,
           frame_id: int,
           frame: np.ndarray,
           *_, **__):
        super().do(frame_id, frame, *_, **__)
        for each_template_name, each_template_path in self.template_dict.items():
            self.fi.load_template(each_template_name, each_template_path)
        res = self.fi.find(str(frame_id), target_pic_object=frame)
        logger.debug(f'compare with template {each_template_name}: {res}')
        self.result[frame_id] = res
