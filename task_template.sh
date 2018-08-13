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