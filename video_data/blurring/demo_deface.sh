#!/bin/bash

#Usage: CUDA_VISIBLE_DEVICES=0 ./demo_deface.sh 201709

path_nas='/home/taehoon/labeling/TraDeS/nas'
video_list=$(cat ./${1}.txt)
for file_name in $video_list; do
    arr=($(echo $file_name | tr "_" "\n")) 
    forder_name=${arr[0]}
    mkdir ${path_nas}/blurring/${forder_name}
    deface ${path_nas}/${forder_name}/${file_name} --output ${path_nas}/blurring/${forder_name}/deface_${file_name}
done
