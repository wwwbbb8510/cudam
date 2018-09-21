class BaseRequest(object):
    """
    base request
    """

    def __init__(self, message):
        """
        init base request
        :param message: the message of the reqeust
        :type message: str
        """
        self._message = message

    def ping(self):
        """
        ping command to check whether the gpu is available on the server
        :return:
        """
        pass

    def run_code(self):
        """
        run the code on the server using gpu
        :return:
        """
        pass

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        self._message = message


class BaseCommand(object):
    """
    base command
    """

    def __init__(self):
        pass

    def execute(self):
        """
        execute the command
        """
        raise NotImplementedError()


class Invoker(object):
    """
    invoke/manage the command
    """

    def __init__(self):
        """
        init the invoker
        """
        self._command = None

    def take_command(self, command):
        """
        init ping command
        :param command: take the command
        :type command: BaseCommand
        """
        self._command = command

    def place_command(self):
        """
        run the command
        """
        self._command.execute()


class PingCommand(BaseCommand):
    """
    ping command
    """

    def __init__(self, request):
        """
        init ping command
        :param request: the request of the command
        :type request: BaseRequest
        """
        super(PingCommand, self).__init__()
        self._request = request

    def execute(self):
        """
        execute the ping command
        """
        self._request.ping()


class RunCodeCommand(BaseCommand):
    def __init__(self, request):
        """
        init ping command
        :param request: the request of the command
        :type request: BaseRequest
        """
        super(RunCodeCommand, self).__init__()
        self._request = request

    def execute(self):
        """
        execute the command to run the code
        """
        self._request.run_code()
