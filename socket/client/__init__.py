import socket
import json
import logging
import numpy as np
from multiprocessing.pool import ThreadPool

from cudam.socket.comm import utils
from .request import ClientRequest


class GPUClientPool(object):
    """
    gpu client pool
    call server to run code in multi-thread mode in a pool
    """
    def __init__(self, server_list):
        """
        init gpu client pool
        :param server_list: server list
        :type server_list: list
        """
        self._server_list = server_list
        self._server_availability = {}

        # check server availability
        self._check_server_availability()

    def run_code_batch(self, arr_args):
        """
        run func
        :param func:
        :param arr_args:
        :return:
        """
        batch_size = len(arr_args)
        batch_result = [None for i in range(batch_size)]
        incomplete_batch_keys = self._search_incomplete_batch_keys(batch_result)
        while len(incomplete_batch_keys) > 0:
            # chunk the args
            # recheck server availability
            self._check_server_availability()
            available_server_list = self._query_available_server_list()
            logging.debug('---The available server list in the batch run---')
            logging.debug('server list: {}'.format(str(available_server_list)))
            len_available_servers = len(available_server_list)

            # retrieve the batch args that need to be ran
            run_keys = incomplete_batch_keys[0: len_available_servers]
            arr_args_to_pass = [arr_args[i] for i in run_keys]

            # attch the ip and port into the args
            for i in range(len(arr_args_to_pass)):
                arr_args_to_pass[i]['ip'], arr_args_to_pass[i]['port'] = available_server_list[i]

            # create pool and run the code in the multi-thread pool
            p = ThreadPool(len_available_servers)
            run_result = p.map(GPUClientPool._run_code_func, arr_args_to_pass)
            p.close()
            p.join()

            # update batch result using run result
            logging.debug('---Run result from the thread pool---')
            logging.debug('run result: {}'.format(str(run_result)))
            self._update_batch_result(batch_result, run_result, run_keys)

            # update incomplete batch keys
            incomplete_batch_keys = self._search_incomplete_batch_keys(batch_result)

        # filter all other information such as error_code apart from result
        batch_response = [response['result'] for response in batch_result]

        return batch_response

    @staticmethod
    def load_server_list_from_file(file):
        loaded_list = np.loadtxt(file, dtype=np.string_, delimiter=',')
        server_list = [(str(server[0].decode()), int(server[1].decode())) for server in loaded_list]
        return server_list


    @staticmethod
    def _search_incomplete_batch_keys(batch_result):
        incomplete_keys = []
        for i in range(len(batch_result)):
            try:
                if batch_result[i]['error_code'] == 0:
                    continue
                else:
                    logging.debug('---Error occurs on cuda server--')
                    logging.debug('response details: {}'.format(str(batch_result[i])))
            except:
                logging.debug('---Exception occurs when passing response from cuda server--')
                logging.debug('response details: {}'.format(str(batch_result[i])))
            incomplete_keys.append(i)
        return incomplete_keys

    @staticmethod
    def _update_batch_result(batch_result, run_result, run_keys):
        for i in range(len(run_result)):
            batch_result[run_keys[i]] = run_result[i]
        return batch_result


    @staticmethod
    def _run_code_func(args):
        ip = args.pop('ip')
        port = args.pop('port')
        g_client = GPUClient(ip, port)
        g_client.connect()
        response = g_client.run('run_code', **args)
        g_client.close()
        return response

    def _check_server_availability(self):
        for ip, port in self._server_list:
            try:
                g_client = GPUClient(ip, port)
                g_client.connect()
                response = g_client.run('ping')
                g_client.close()
                if type(response) == dict and 'availability' in response.keys() and response['availability'] > 0:
                    self._server_availability[(ip, port)] = True
                else:
                    self._server_availability[(ip, port)] = False
            except:
                self._server_availability[(ip, port)] = False
        return self._server_availability

    def _query_available_server_list(self):
        available_server_list = [key for key in self.server_availability.keys() if
                                 self.server_availability[key] is True]
        return available_server_list


    @property
    def server_availability(self):
        return self._server_availability


class GPUClient(object):
    """
    gpu client
    """

    def __init__(self, ip, port):
        """
        init gpu socket client
        :param ip: server ip
        :type ip: str
        :param port: server port
        :type port: int
        """
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
        try:
            self.socket.sendall(request_str.encode())
            response_str = utils.recvall(self.socket).decode()
            logging.debug('---data received:{} ---'.format(response_str))
            response_data = json.loads(response_str) if len(response_str) > 0 else {}
        except:
            logging.debug('---run command failed---')
            response_data = None
        return response_data

    def __del__(self):
        if self.socket is not None:
            logging.debug(
                '---Close the socket connection in the __del__ function. IP:{}, port:{}---'.format(self.ip, self.port))
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
