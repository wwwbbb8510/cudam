from ..comm.message import BaseRequest


class ClientRequest(BaseRequest):
    def __init__(self):
        super(ClientRequest, self).__init__('')

    def ping(self):
        return {}

    def run_code(self):
        pass
