import logging
import threading
import datetime


def debug(msg, *args, **kwargs):
    cur_thread = threading.current_thread()
    str_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = 'Thread: {}, Time:{}, msg: {}'.format(cur_thread.name, str_time, msg)
    logging.debug(msg, *args, **kwargs)
