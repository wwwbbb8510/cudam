class BaseRequest(object):
    """
    base request
    """

    def __init__(self):
        """
        init base request
        """
        pass

    def ping(self):
        """
        ping command to check whether the gpu is available on the server
        :return: the availability of the cuda gpus
        :rtype: dict
        """
        pass

    def run_code(self, path, entry, args, work_directory, use_cuda=True):
        """
        run the code on the server using gpu
        :param path: the path of the code to be executed
        :type path: str
        :param entry: the entry function to be executed
        :type entry: str
        :param args: the arguments that are passed to the entry function
        :type args: dict
        :param work_directory: working directory of the code to be ran
        :type work_directory: str
        :param use_cuda: whether to use cuda gpus
        :type use_cuda: bool
        :return: the results of the executed function
        :rtype: dict
        """
        pass
