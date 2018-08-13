import glob
import logging
import os
import time
import subprocess


class ShellTaskList(object):
    # the processed task list shared across all objects
    _processed_tasks = []

    def __init__(self, task_path):
        """
        initialise
        :param task_path: the path where the tasks reside
        :type task_path: str
        """
        self._task_path = task_path
        self._all_task_list = None
        self._task_list = None

    @staticmethod
    def append_processed_task(task):
        """
        append a processed tasks in the processed_task list
        :param task: the processed task
        :type task: ShellTask
        """
        ShellTaskList._processed_tasks.append(task)

    @staticmethod
    def fetch_newly_processed_tasks(freezing_period=300):
        return [task for task in ShellTaskList._processed_tasks if
         task.start_time is not None and time.time() - task.start_time < freezing_period]

    def load_tasks(self):
        """
        load the task list that haven't been processed
        :return: a list of the unprocessed tasks
        :rtype: list
        """
        self.load_all_tasks()
        self._task_list = list(set(self.all_task_list) - set(ShellTaskList._processed_tasks))
        return self.task_list

    def load_all_tasks(self):
        """
        load the tasks from task folder
        :return: a list of task files in the task path
        :rtype: list
        """
        files = glob.glob(os.path.join(self.task_path, '*.sh'))
        logging.debug('load sh task files in the folder:%s', self.task_path)

        self._all_task_list = []
        for file in files:
            self._all_task_list.append(ShellTask(file))
        return self.all_task_list

    @property
    def task_list(self):
        return self._task_list

    @property
    def all_task_list(self):
        return self._all_task_list

    @property
    def task_path(self):
        return self._task_path

    @task_path.setter
    def task_path(self, task_path):
        self._task_path = task_path


class ShellTask(object):
    def __init__(self, file_path):
        """
        initialise
        :param file_path: the file path of the task
        :type file_path: str
        """
        self._file_path = file_path
        self._cuda_id = None
        self._start_time = None

    def run_task(self):
        """
        run the task using bash
        :return: output the script
        """
        output = subprocess.call('bash ' + self.file_path + ' -g ' + str(self.cuda_id), shell=True)
        return output

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    @property
    def cuda_id(self):
        return self._cuda_id

    @cuda_id.setter
    def cuda_id(self, cuda_id):
        self._cuda_id = cuda_id

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    def __hash__(self):
        return hash(self._file_path)

    def __eq__(self, other):
        return self.file_path == other.file_path

    def __repr__(self):
        str_repr = super(ShellTask, self).__repr__() + os.linesep
        str_repr += 'File:{}'.format(self.file_path)
        str_repr += os.linesep
        str_repr += 'Cuda ID:{}'.format(self.cuda_id)
        str_repr += os.linesep
        str_repr += 'Start time:{}'.format(self.start_time)
        str_repr += os.linesep
        return str_repr
