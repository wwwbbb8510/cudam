from ..comm.message import BaseRequest


class ClientRequest(BaseRequest):
    def __init__(self):
        super(ClientRequest).__init__(None)

    def ping(self):
        pass

    def run_code(self):
        pass
