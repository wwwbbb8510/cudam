import logging

from ..comm.message import BaseRequest


class ClientRequest(BaseRequest):
    """
    client request
    """
    def __init__(self):
        """
        init client request
        """
        super(ClientRequest, self).__init__()

    def ping(self, use_cuda=True):
        logging.debug('---ping command called---')
        dict_request = {}
        return dict_request

    def run_code(self, path, entry='main', args=None, work_directory=None, use_cuda=True):
        logging.debug('---run_code command called---')
        dict_request = {
            'path': path,
            'entry': entry,
            'args': args,
            'work_directory': work_directory,
            'use_cuda': use_cuda
        }
        logging.debug('---run_code command request---')
        logging.debug(dict_request)
        return dict_request
