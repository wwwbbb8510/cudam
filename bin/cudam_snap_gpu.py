#!/usr/bin/env python
import argparse
import logging

from cudam.cuda.gpu import utils as gu
import time
import os

# nohup python cudam_sp_gpu.py -s 1 -l 300 -i 60 -g 0 &

def main(args):
    _filter_args(args)
    # configure logging
    log_file_path = 'log/main_task_manager_snap_' + args.server + '.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)
    logging.info('===Snap gpu - server:%s, gpu:%d===', args.server, args.gpu)

    # snap gpu resource
    while True:
        if args.gpu is not None:
            os.environ['CUDA_VISIBLE_DEVICES'] = '{}'.format(args.gpu)
            gu.snap_gpu(args.gpu, args.lock_time)
            time.sleep(args.interval)


def _filter_args(args):
    """
    filter the arguments

    :param args: arguments
    """
    args.server = str(args.server) if args.server is not None else None
    args.lock_time = int(args.lock_time) if args.lock_time is not None else None
    args.gpu = int(args.gpu) if args.gpu is not None else None
    args.interval = int(args.interval) if args.interval is not None else 30


# main entrance
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help='server id where the script will be running')
    parser.add_argument('-l', '--lock_time', help='available GPU lock time')
    parser.add_argument('-g', '--gpu', help='gpu ID')
    parser.add_argument('-i', '--interval', help='interval')
    args = parser.parse_args()
    main(args)
