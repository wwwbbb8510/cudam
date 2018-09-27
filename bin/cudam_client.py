import logging
import argparse
import os

from cudam.socket.client import GPUClient

# pythonpath.bat C:\\code\\exercises\\COMP489 cudam/bin/cudam_client.py
DEFAULT_COMMAND = 'run_code'

DEFAULT_RUN_CODE_PATH = "cudam.bin.cudam_run_code_dumb"
if os.name == 'nt':
    DEFAULT_RUN_CODE_WORK_DIRECTORY = "C:\\code\\exercises\\COMP489"
else:
    DEFAULT_RUN_CODE_WORK_DIRECTORY = "/home/wangbin/code/comp489"

def main(args):
    _filter_args(args)
    # configure logging
    log_file_path = 'log/cudam_client_' + args.client + '.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    logging.debug('===Start client. ID:{}, IP:{}, port==='.format(args.client, args.ip, args.port))

    # start the client
    g_client = GPUClient(args.ip, args.port)
    g_client.connect()
    logging.debug('===Test command:{}==='.format(args.command))
    if args.command == 'run_code':
        response = g_client.run(args.command, path=DEFAULT_RUN_CODE_PATH, work_directory=DEFAULT_RUN_CODE_WORK_DIRECTORY, use_cuda=False)
    else:
        response = g_client.run(args.command)
    print(response)


def _filter_args(args):
    """
    filter the arguments

    :param args: arguments
    """
    args.client = str(args.client) if args.client is not None else ''
    args.ip = str(args.ip) if args.ip is not None else 'localhost'
    args.port = int(args.port) if args.port is not None else 8000
    args.command = str(args.command) if args.command is not None else DEFAULT_COMMAND


# main entrance
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', help='the client ID')
    parser.add_argument('-i', '--ip', help='host IP, default: localhost')
    parser.add_argument('-p', '--port', help='port, default: 8000')
    parser.add_argument('-d', '--command', help='command, default: ping')
    args = parser.parse_args()
    main(args)
