import threading
import socketserver
import json
import cudam.socket.comm.logging as logging
import os

from .request import ServerRequest
from cudam.socket.comm import utils


class GPUServer(object):
    # the dataset used by the server
    _dataset = None

    def __init__(self, ip, port, gpu_id):
        logging.debug('---Start server. IP:{}, port:{}---'.format(ip, port))
        self._ip = ip
        self._port = port
        self._gpu_id = gpu_id
        # set available gpu
        self._set_visible_gpu()
        # create the socket server
        self._server = GPUServerSocket((self.ip, self.port), GPUServerRequestHandler)

    def _set_visible_gpu(self):
        """
        set visible gpu id
        :return:
        """
        if self.gpu_id >= 0:
            os.environ['CUDA_VISIBLE_DEVICES'] = '{}'.format(self.gpu_id)
            logging.debug('---Cuda {} is set visible---'.format(self.gpu_id))
            ServerRequest._init_cuda_queue(self.gpu_id)

    def start(self):
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        logging.debug("---Server loop running in thread:{}---".format(server_thread.name))
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

    def stop(self):
        logging.debug('---Stop server. IP:{}, port:{}---'.format(self.ip, self.port))
        self.server.shutdown()
        self.server.server_close()
        self._server = None

    def __del__(self):
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            logging.debug('---Stop server. IP:{}, port:{} in the __del__ function---'.format(self.ip, self.port))

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def gpu_id(self):
        return self._gpu_id

    @property
    def server(self):
        return self._server

    @property
    def dataset(self):
        return GPUServer._dataset

    @staticmethod
    def get_dataset():
        return GPUServer._dataset

    @dataset.setter
    def dataset(self, dataset):
        GPUServer._dataset = dataset



class GPUServerSocket(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class GPUServerRequestHandler(socketserver.BaseRequestHandler):
    _command_request = None

    def handle(self):
        cur_thread = threading.current_thread()
        json_str = utils.recvall(self.request).decode()
        logging.debug('---Thread:{} is handling the request---'.format(cur_thread.name))
        logging.debug('---data received:{} ---'.format(str(json_str)))
        data = json.loads(json_str) if len(json_str) > 0 else {}
        # pop command from data
        command = data['command']
        del (data['command'])
        # add server dataset into data['args']
        if command != 'ping':
            if 'args' not in data.keys():
                data['args'] = {}
            data['args']['dataset'] = GPUServer.get_dataset()
        response_data = getattr(self.command_request, command)(**data)
        response_data['cur_thread'] = cur_thread.name
        response_str = json.dumps(response_data)
        logging.debug('---data sent:{} ---'.format(response_str))
        self.request.sendall(response_str.encode())

    @property
    def command_request(self):
        if GPUServerRequestHandler._command_request is None:
            logging.debug('---instantiate the server request---')
            GPUServerRequestHandler._command_request = ServerRequest()
        return GPUServerRequestHandler._command_request
