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
nohup cudam_task_manager -n 2 -s 2 -i 10 -f 300 -l 60 &
# snap gpu
python3 cudam_snap_gpu -s 2 -l 60 -g 1
```
