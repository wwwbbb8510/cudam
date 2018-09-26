import socket
import json
from .request import ClientRequest


class GPUClient(object):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._request = ClientRequest()

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def close(self):
        self.socket.close()
        self._socket = None

    def run(self, command, **kwargs):
        request_data = getattr(self.request, command)(**kwargs)
        request_data['command'] = command
        request_str = json.dumps(request_data)
        self.socket.sendall(request_str.encode())
        response_str = self.socket.recv(1024)
        response_data = json.loads(response_str.decode())
        return response_data

    def __del__(self):
        if self.socket is not None:
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
