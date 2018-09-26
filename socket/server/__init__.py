import threading
import socketserver
import json
from .request import ServerRequest


class GPUServer(object):
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._server = GPUServerSocket((self.ip, self.port), GPUServerRequestHandler)

    def start(self):
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self._server = None

    def __del__(self):
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def server(self):
        return self._server


class GPUServerSocket(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class GPUServerRequestHandler(socketserver.BaseRequestHandler):
    _command_request = None

    def handle(self):
        json_str = self.request.recv(1024)
        data = json.loads(json_str.decode())
        command = data['command']
        del (data['command'])
        response_data = getattr(self.command_request, command)(**data)
        cur_thread = threading.current_thread()
        response_data['cur_thread'] = cur_thread.name
        response_str = json.dumps(response_data)
        self.request.sendall(response_str.encode())

    @property
    def command_request(self):
        if GPUServerRequestHandler._command_request is None:
            GPUServerRequestHandler._command_request = ServerRequest()
        return GPUServerRequestHandler._command_request
