from ..comm.message import BaseRequest


class ServerRequest(BaseRequest):
    def __init__(self):
        super(ServerRequest).__init__(None)

    def ping(self):
        pass

    def run_code(self):
        pass
