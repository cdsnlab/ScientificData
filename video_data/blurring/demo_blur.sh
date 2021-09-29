#!/bin/bash

#Usage: CUDA_VISIBLE_DEVICES=0 ./demo_blur.sh 201709

path_nas='/home/taehoon/labeling/TraDeS/nas'
video_list=$(cat ./${1}.txt)
for file_name in $video_list; do
    arr=($(echo $file_name | tr "_" "\n")) 
    forder_name=${arr[0]}
    mkdir ${path_nas}/blurring/${forder_name}
    xvfb-run -a python auto_blur_video.py --input_video ${path_nas}/${forder_name}/${file_name}\
                                       --output_video ${path_nas}/blurring/${forder_name}/blur_${file_name}\
                                       --model_path ../face_model/face.pb\
                                       --threshold 0.1
done
