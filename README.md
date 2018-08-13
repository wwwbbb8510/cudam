# cudam
Cuda Mangement - multi-process, scheduled jobs, distributed processing

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
```

* Run the task manager
```bash
# run interactively
python cudam_task_manager.py -n 2 -s 2 -i 60 -f 300
# run in background
nohup python cudam_task_manager.py -n 2 -s 2 -i 60 -f 300 &
```

