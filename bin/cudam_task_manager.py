#!/usr/bin/env python
import argparse
import logging
import time
import _thread
import subprocess
import os

from cudam.cuda.gpu import utils as gu
from cudam.cuda.task import shell_task as st

def main(args):
    _filter_args(args)
    # set constants
    task_folder = os.path.join('log', 'tasks', args.server)
    # configure logging
    log_file_path = 'log/main_task_manager_' + args.server + '.log'
    logging.basicConfig(filename=log_file_path, level=logging.DEBUG)

    logging.info('===Start task manager - server:%s, gpu range:%d===', args.server, args.number)

    search_ids = list(range(0, args.number))
    while True:
        # check available gpus
        available_gpus = gu.search_available_gpus(search_ids, debug=args.debug)
        available_gpus = remove_gpu_for_newly_processed_tasks(available_gpus, args.freeze_period)
        # used gpus
        used_gpus = []

        if len(available_gpus) > 0:
            # load task from task folder
            task_list = st.ShellTaskList(task_folder).load_tasks()
            task_num = min(len(available_gpus), len(task_list))
            for gpu_index in range(0, task_num):
                task_list[gpu_index].cuda_id = available_gpus[gpu_index]
                task_list[gpu_index].start_time = time.time()
                logging.debug('===Start to run task:%s on gpu:%d===', task_list[gpu_index], available_gpus[gpu_index])
                _thread.start_new_thread(task_list[gpu_index].run_task, ())
                st.ShellTaskList.append_processed_task(task_list[gpu_index])
                used_gpus.append(available_gpus[gpu_index])

            # occupy available gpus
            available_gpus_after = list(set(available_gpus) - set(used_gpus))
            if args.lock_time is not None and args.lock_time > 0:
                for gpu_id_after in available_gpus_after:
                    logging.debug('===Start to snap gpu:%d for seconds:%d===', gpu_id_after, args.lock_time)
                    _thread.start_new_thread(snap_gpu_by_process, (gpu_id_after, args.lock_time, args.server))

        logging.info('Main thread starts to sleep for %d seconds', args.interval)
        time.sleep(args.interval)


def remove_gpu_for_newly_processed_tasks(available_gpus, freeze_period=300):
    """
    remove the gpu which will be used by the tasks (allow task to take 300 seconds to take up the gpu)
    :param available_gpus: the available gpu list
    :type available_gpus: list
    :param freeze_period: after the task starts, freeze the gpu for a period
    :type freeze_period: int
    :return: the available gpus after removing the gpus in the freeze period
    :rtype: list
    """
    newly_processed_tasks = st.ShellTaskList.fetch_newly_processed_tasks(freeze_period)
    newly_used_cuda_ids = [task.cuda_id for task in newly_processed_tasks if task.cuda_id is not None]
    available_gpus = list(set(available_gpus) - set(newly_used_cuda_ids))
    return available_gpus


def snap_gpu_by_process(gpu_id, lock_time, server):
    """
    snap gpu
    :param gpu_id: gpu id
    :type gpu_id: int
    :param lock_time: the time period that the gpu is snapped
    :type lock_time: int
    :param server: server id
    :type server: int
    :return:
    """
    str_command = 'python cudam_snap_gpu.py -s {} -l {} -g {}'.format(server, lock_time, gpu_id)
    arr_command = str_command.split(' ')
    output = subprocess.call(arr_command)
    return output


def _filter_args(args):
    """
    filter the arguments

    :param args: arguments
    """
    args.number = int(args.number) if args.number is not None else None
    args.server = str(args.server) if args.server is not None else None
    args.interval = int(args.interval) if args.interval is not None else 30
    args.freeze_period = int(args.freeze_period) if args.freeze_period is not None else 300
    args.lock_time = int(args.lock_time) if args.lock_time is not None else None
    args.debug = True if args.debug is not None and int(args.debug) > 0 else False


# main entrance
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help='total gpu number that will be used')
    parser.add_argument('-s', '--server', help='server id where the script will be running')
    parser.add_argument('-i', '--interval', help='set the interval to search available gpu')
    parser.add_argument('-f', '--freeze_period', help='the freeze period from when a task starts to run')
    parser.add_argument('-l', '--lock_time', help='available GPU lock time')
    parser.add_argument('-d', '--debug', help='debug')
    args = parser.parse_args()
    main(args)
