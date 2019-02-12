# cudam
Cuda Mangement - multi-process, scheduled jobs, distributed processing

## command to check all cuda server status

```bash
date >> cuda_status.txt && echo 'cuda1' >> cuda_status.txt && ssh cuda1 'nvidia-smi' >> cuda_status.txt && echo 'cuda2' >> cuda_status.txt && ssh cuda2 'nvidia-smi' >> cuda_status.txt && echo 'cuda3' >> cuda_status.txt && ssh cuda3 'nvidia-smi' >> cuda_status.txt && echo 'cuda4' >> cuda_status.txt && ssh cuda4 'nvidia-smi' >> cuda_status.txt && echo 'cuda5' >> cuda_status.txt && ssh cuda5 'nvidia-smi' >> cuda_status.txt && echo 'cuda6' >> cuda_status.txt && ssh cuda6 'nvidia-smi' >> cuda_status.txt && echo 'cuda11' >> cuda_status.txt && ssh cuda11 'nvidia-smi' >> cuda_status.txt
```

## server-client mode to utilize multi-GPUs across Multi-Machines

### server side - develop the code that runs on a single GPU

```python
# here is a dumb function to evaluate densenet
# it should be replaced by the actual code of evaluation
def evaluate_densenet(model):
    acc = 0.99
    return acc
```

### client size - develop the code to send the models to server for evaluation

* Add available GPU servers in the server list configuration file

```text
# configuration of server list
cuda4,8000
cuda4,8001
cuda5,8000
cuda5,8001
cuda5,8002
```

* The client code that concurrently evaluates models

```python
from cudam.socket.client import GPUClientPool
DEFAULT_RUN_CODE_WORK_DIRECTORY = "/home/www/server" # the folder where the server side code resides 
DEFAULT_RUN_CODE_PATH = "server_file" # the file name of the server side code
SERVER_LIST_CONFIG = 'config/server_list.txt' # the configuration file of the server list
def pool_evaluate_densenet(model_list):
    # generat the arguments which will passed to client pool
    arr_args = []
    for m in model_list:        
        singe_args = {'model': m}
        arr_args.append({
            'path': DEFAULT_RUN_CODE_PATH,
            'entry': "evaluate_densenet",
            'work_directory': DEFAULT_RUN_CODE_WORK_DIRECTORY,
            'args': singe_args,
            'use_cuda': True # whether to use GPU or not
        })
    # init client pool
    server_list = GPUClientPool.load_server_list_from_file(SERVER_LIST_CONFIG)
    pool = GPUClientPool(server_list)
    # perform evaluation
    eval_result = pool.run_code_batch(arr_args)
    return eval_result
# main entrance
if __name__ == '__main__':
    model_list =[] # dumb model list which needs to be replaced by real models
    pool_evaluate_densenet(model_list)
```

### start the server 

* After installation of this package, `cudam_server.py` should be automatically copied to the bin path; if not, please manually copy this file to the root folder of the project. The server can be started by running the following command:  

### run the client side python code to evaluate a batch of models

```bash
cudam_socket
nohup python cudam_server.py -s 1 -i cuda1 -p 8000 -g 0 >& log/nohup_cuda_1_8000_0.log &
```



## task manager

### task template

```bash
#!/usr/bin/env bash

while getopts g: option;do
    case "${option}" in
    g) GPU_ID=${OPTARG};;
    esac
done

print_help(){
    printf "Parameter g(GPU ID) is mandatory\n"
    printf "g values - GPU ID"
    exit 1
}

if [ -z "${GPU_ID}" ];then
    print_help
fi

echo "start task on GPU: $GPU_ID"

# the root directory of your python script
cd ~/code/psocnn/
# the main python script accepting the gpu ID in -g argument
python3 main.py -g ${GPU_ID}
```

### task folder structure

![task folder structure](https://github.com/wwwbbb8510/cudam/blob/master/sh_task_structure.PNG "Task folder structure")

### task manager 

```bash
# start task manager
nohup cudam_task_manager.py -n 2 -s 2 -i 60 -f 300 &
# snap gpu
cudam_snap_gpu.py -s 2 -l 60 -g 1
```

### install cumdam for a specific user and can not add the local path into executable PATH

* Switch to the root folder of your project

* Install cudam package
```bash
pip install --user cudam
``` 

* Create a soft link of the executable file
```bash
ln -s /home/{YOURUSER}/.local/bin/cudam_task_manager.py cudam_task_manager.py
ln -s /home/{YOURUSER}/.local/bin/cudam_snap_gpu.py cudam_snap_gpu.py
```

* Run the task manager
```bash
# run interactively
python cudam_task_manager.py -n 2 -s 2 -i 60 -f 300
# run in background
nohup python cudam_task_manager.py -n 2 -s 2 -i 60 -f 300 &
```

