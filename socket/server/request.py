import torch
import queue
import sys
import logging

from ..comm.message import BaseRequest
from cudam.cuda.gpu import utils


class ServerRequest(BaseRequest):
    """
    server request
    """
    # the queue contains the available cuda gpus
    _cuda_queue = None

    def __init__(self):
        """
        init server request
        """
        super(ServerRequest, self).__init__()

    def ping(self):
        logging.debug('---ping command called---')
        dict_response = {'availability': self.cuda_queue.qsize()}
        logging.debug('---ping command response---')
        logging.debug(dict_response)
        return dict_response

    def run_code(self, path, entry, args, work_directory, use_cuda=True):
        logging.debug('---run_code command called---')
        is_device_ready = False
        cuda_id = None
        if use_cuda:
            if not self.cuda_queue.empty():
                cuda_id = self.cuda_queue.get(False)
                if cuda_id is not False:
                    is_device_ready = True
        else:
            is_device_ready = True

        if is_device_ready:
            if cuda_id is not None:
                torch.cuda.set_device(cuda_id)
            torch.cuda.empty_cache()
            sys.path.append(work_directory)
            exec("import " + path + " as run_code_module")
            module_obj = eval("run_code_module")
            result = getattr(module_obj, entry)(**args)
            logging.debug('---run_code calling details---')
            logging.debug(
                'path:{}, entry:{}, args:{}, work_directory:{}, use_cuda:{}'.format(path, entry, str(args),
                                                                                    work_directory, use_cuda))
            dict_response = {
                'result': result,
                'error_code': 0,
                'error_message': ''
            }
            if not self.cuda_queue.full():
                self.cuda_queue.put(cuda_id)
        else:
            dict_response = {
                'result': None,
                'error_code': 1,
                'error_message': 'no available gpus/devices'
            }

        logging.debug('---run_code command response---')
        logging.debug(dict_response)

        return dict_response

    @property
    def cuda_queue(self):
        """
        get the property: cuda_queue
        :return: cuda queue
        :rtype: queue.Queue
        """
        if ServerRequest._cuda_queue is None:
            ServerRequest._init_cuda_queue()
        return ServerRequest._cuda_queue

    @staticmethod
    def _init_cuda_queue():
        logging.debug('---initialise the cuda queue---')
        if torch.cuda.is_available() and torch.cuda.device_count() > 0:
            ServerRequest._cuda_queue = queue.Queue(torch.cuda.device_count())
            logging.debug('---{} cuda gpus are found---'.format(torch.cuda.device_count()))
            for i in range(torch.cuda.device_count()):
                if utils.ping_gpu(i):
                    ServerRequest._cuda_queue.put(i)
                    logging.debug('---cuda:{} is added in the queue---'.format(i))
        else:
            ServerRequest._cuda_queue = queue.Queue(1)