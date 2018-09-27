from cudam.socket.server import GPUServer
import argparse
import logging


# pythonpath.bat C:\\code\\exercises\\COMP489 cudam/bin/cudam_server.py
def main(args):
    _filter_args(args)
    # configure logging
    log_file_path = 'log/cudam_server_' + args.server + '.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    logging.debug('===start server. ID:{}, IP:{}, port:{}==='.format(args.server, args.ip, args.port))

    # start the server
    g_server = GPUServer(args.ip, args.port)
    g_server.start()


def _filter_args(args):
    """
    filter the arguments

    :param args: arguments
    """
    args.server = str(args.server) if args.server is not None else ''
    args.ip = str(args.ip) if args.ip is not None else 'localhost'
    args.port = int(args.port) if args.port is not None else 8000


# main entrance
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help='the server ID')
    parser.add_argument('-i', '--ip', help='host IP, default: localhost')
    parser.add_argument('-p', '--port', help='port, default: 8000')
    args = parser.parse_args()
    main(args)
