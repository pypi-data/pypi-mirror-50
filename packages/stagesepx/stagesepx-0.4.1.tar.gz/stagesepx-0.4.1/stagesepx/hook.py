import numpy as np


class Hook(object):
    def __init__(self, *_, **__):
        self.result = None

    def do(self, frame: np.ndarray, *_, **__):
        raise NotImplementedError('MUST IMPLEMENT THIS FIRST')
