name = "cudam"
__all__ = ['cuda']

import os
import logging

def set_visible_gpu(gpu_id):
    """
    set visible gpu id
    :return:
    """
    if gpu_id >= 0:
        os.environ['CUDA_VISIBLE_DEVICES'] = '{}'.format(gpu_id)
        logging.debug('---Cuda {} is set visible---'.format(gpu_id))