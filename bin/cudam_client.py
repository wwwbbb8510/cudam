from cudam.socket.client import GPUClient
import logging
import argparse


# pythonpath.bat C:\\code\\exercises\\COMP489 cudam/bin/cudam_client.py
def main(args):
    _filter_args(args)
    # configure logging
    log_file_path = 'log/cudam_client' + args.client + '.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    logging.info('===Start client - client:%s===', args.client)

    # start the server
    g_client = GPUClient(args.ip, args.port)
    g_client.connect()
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
    args.command = str(args.command) if args.command is not None else 'ping'


# main entrance
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', help='the client ID')
    parser.add_argument('-i', '--ip', help='host IP, default: localhost')
    parser.add_argument('-p', '--port', help='port, default: 8000')
    parser.add_argument('-d', '--command', help='command, default: ping')
    args = parser.parse_args()
    main(args)
