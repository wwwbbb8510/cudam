import torch
import logging
import time
import subprocess
import re


def search_available_gpus(search_ids=None, **kwargs):
    """
    search available gpus
    :param search_ids: the gpu IDs which are searched for
    :type search_ids: list
    :return: a list of available gpus
    :rtype: list
    """
    search_ids = [0, 1] if search_ids is None else search_ids
    used_gpus = search_used_gpus(**kwargs)
    available_gpus = list(set(search_ids) - set(used_gpus))

    return available_gpus


def search_used_gpus(debug=False):
    """
    search used gpus through nvidia-smi command
    :param debug: debug mode
    :type debug: bool
    :return: a list of used gpus
    :rtype: list
    """
    used_gpus = []
    if debug:
        # str_output = '|    0      6420      C   python3                                     7865MiB |\n|    1      1919      C   python3.6                                   7435MiB |'
        str_output = '|    0      6420      C   python3                                     7865MiB |'
    else:
        nv_output = subprocess.check_output('nvidia-smi', shell=True)
        str_output = nv_output.decode('utf-8')
    arr_output = str_output.split('\n')
    for str_row in arr_output:
        match_obj = re.match(r'\|\s+(\d)\s+\d+\s+\w+\s+[\w\d.]+\s+\d+MiB\s+\|', str_row)
        if match_obj is not None:
            used_gpus.append(int(match_obj.group(1)))
    logging.debug('used gpus:{}'.format(used_gpus))

    return used_gpus


def ping_gpu(cuda_id):
    """
    ping gpu to see whether the gpu with cuda_id is available or not
    :param cuda_id: cuda id
    :type cuda_id: int
    :return: whether the cuda gpu is available or nto
    :rtype: bool
    """
    flag = False
    try:
        torch.ones(1).cuda(cuda_id)
        flag = True
    except:
        logging.debug('cuda:{} is not available'.format(cuda_id))

    return flag


def snap_gpu(cuda_id, delay=60):
    """
    snap the gpu for a number of seconds
    :param cuda_id: cuda ID
    :type cuda_id: int
    :param delay: the time period to snap the gpu
    :type delay: int
    """
    try:
        torch.ones(1).cuda(cuda_id)
        time.sleep(delay)
    except:
        logging.debug('fail to snap cuda:{}'.format(cuda_id))


def free_gpu_memory():
    """
    explicitly free gpu memory
    """
    torch.cuda.empty_cache()
