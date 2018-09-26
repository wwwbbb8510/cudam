import torch
import queue
from ..comm.message import BaseRequest
from cudam.cuda.gpu import utils


class ServerRequest(BaseRequest):
    _cuda_queue = None

    def __init__(self):
        super(ServerRequest, self).__init__('')

    def ping(self):
        return {'availability': self.cuda_queue.qsize()}

    def run_code(self):
        pass

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
        if torch.cuda.is_available() and torch.cuda.device_count() > 0:
            ServerRequest._cuda_queue = queue.Queue(torch.cuda.device_count())
            for i in range(torch.cuda.device_count()):
                if utils.ping_gpu(i):
                    ServerRequest._cuda_queue.put(i)
        else:
            ServerRequest._cuda_queue = queue.Queue(1)
