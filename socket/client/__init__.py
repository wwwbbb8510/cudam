import socket
import json
import logging

from .request import ClientRequest


class GPUClient(object):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        logging.debug('---Start client. IP:{}, port:{}---'.format(ip, port))
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._request = ClientRequest()

    def connect(self):
        logging.debug('---Connect to the server. IP:{}, port:{}---'.format(self.ip, self.port))
        self.socket.connect((self.ip, self.port))

    def close(self):
        logging.debug('---Close the socket connection. IP:{}, port:{}---'.format(self.ip, self.port))
        self.socket.close()
        self._socket = None

    def run(self, command, **kwargs):
        request_data = getattr(self.request, command)(**kwargs)
        request_data['command'] = command
        request_str = json.dumps(request_data)
        logging.debug('---data sent:{} ---'.format(request_str))
        self.socket.sendall(request_str.encode())
        response_str = self.socket.recv(1024).decode()
        logging.debug('---data received:{} ---'.format(response_str))
        response_data = json.loads(response_str) if len(response_str) > 0 else {}
        return response_data

    def __del__(self):
        if self.socket is not None:
            logging.debug('---Close the socket connection in the __del__ function. IP:{}, port:{}---'.format(self.ip, self.port))
            self.close()

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def socket(self):
        return self._socket

    @property
    def request(self):
        return self._request
