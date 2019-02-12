import argparse
import logging

from cudam.cudam_socket.server import GPUServer
from bidcap.utils.loader import ImagesetLoader

DEBUG = 0


# pythonpath.bat C:\\code\\exercises\\COMP489 cudam/bin/cudam_server.py
# nohup python cudam_server.py -s 1 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda1.sms.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_1_8000_0.log &
# nohup python cudam_server.py -s 1 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda1.sms.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_1_8001_1.log &
# nohup python cudam_server.py -s 2 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda2.sms.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_2_8000_0.log &
# nohup python cudam_server.py -s 2 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda2.sms.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_2_8001_1.log &
# nohup python cudam_server.py -s 3 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda3.sms.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_3_8000_0.log &
# nohup python cudam_server.py -s 3 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda3.sms.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_3_8001_1.log &
# nohup python cudam_server.py -s 4 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda4.sms.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_4_8000_0.log &
# nohup python cudam_server.py -s 4 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda4.sms.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_4_8001_1.log &
# nohup python cudam_server.py -s 5 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda5.ecs.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_5_8000_0.log &
# nohup python cudam_server.py -s 5 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda5.ecs.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_5_8001_1.log &
# nohup python cudam_server.py -s 5 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda5.ecs.vuw.ac.nz -p 8002 -g 2 >& log/nohup_cudam_server_5_8002_2.log &
# nohup python cudam_server.py -s 6 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda6.ecs.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_6_8000_0.log &
# nohup python cudam_server.py -s 6 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda6.ecs.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_6_8001_1.log &
# nohup python cudam_server.py -s 6 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda6.ecs.vuw.ac.nz -p 8002 -g 2 >& log/nohup_cudam_server_6_8002_2.log &
# nohup python cudam_server.py -s 11 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda11.ecs.vuw.ac.nz -p 8000 -g 0 >& log/nohup_cudam_server_11_8000_0.log &
# nohup python cudam_server.py -s 11 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda11.ecs.vuw.ac.nz -p 8001 -g 1 >& log/nohup_cudam_server_11_8001_1.log &
# nohup python cudam_server.py -s 11 --partial_dataset_ratio=1 --train_validation_split_point=40000 -i cuda11.ecs.vuw.ac.nz -p 8002 -g 2 >& log/nohup_cudam_server_11_8002_2.log &
def main(args):
    _filter_args(args)
    # configure logging
    log_file_path = 'log/cudam_server_' + args.server + '_' + str(args.port) + '_' + str(args.gpu_id) + '.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    logging.debug('===start server. ID:{}, IP:{}, port:{}==='.format(args.server, args.ip, args.port))

    # load dataset
    dataset = _load_dataset(args.dataset_name, args.partial_dataset_ratio, args.train_validation_split_point)

    # start the server
    g_server = GPUServer(args.ip, args.port, args.gpu_id)
    g_server.dataset = dataset
    g_server.start()


def _filter_args(args):
    """
    filter the arguments

    :param args: arguments
    """
    args.server = str(args.server) if args.server is not None else ''
    args.ip = str(args.ip) if args.ip is not None else 'localhost'
    args.port = int(args.port) if args.port is not None else 8000
    args.gpu_id = int(args.gpu_id) if args.gpu_id is not None else 0
    args.dataset_name = str(args.dataset_name) if args.dataset_name is not None else 'cifar10'
    args.train_validation_split_point = int(
        args.train_validation_split_point) if args.train_validation_split_point is not None else 4000
    args.partial_dataset_ratio = float(args.partial_dataset_ratio) if args.partial_dataset_ratio is not None else 0.1


def _load_dataset(dataset_name, partial_dataset_ratio, train_validation_split_point):
    # load dataset
    mode = 0 if DEBUG == 1 else None
    train_validation_split_point = 800 if DEBUG else train_validation_split_point
    dataset = ImagesetLoader.load(dataset_name,
                                  train_validation_split_point=train_validation_split_point,
                                  partial_dataset_ratio=partial_dataset_ratio,
                                  mode=mode)
    return dataset


# main entrance
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help='the server ID')
    parser.add_argument('-i', '--ip', help='host IP, default: localhost')
    parser.add_argument('-p', '--port', help='port, default: 8000')
    parser.add_argument('-g', '--gpu_id', help='GPU ID, default: 0')
    parser.add_argument('--dataset_name',
                        help='dataset names:{}. Default: cifar10'.format(ImagesetLoader.dataset_classes().keys()))
    parser.add_argument('--train_validation_split_point', help='train validation split point, default: 4000')
    parser.add_argument('--partial_dataset_ratio', help='partial dataset ratio, default: 0.1')
    args = parser.parse_args()
    main(args)
