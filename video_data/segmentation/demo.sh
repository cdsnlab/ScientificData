#!/bin/bash

#Usage: ./demo.sh ../nas 201903
FOLDER_LIST=$(ls ${1} | grep ^${2})

for FOLDER in $FOLDER_LIST; do
    FILE_LIST=$(ls ${1}/${FOLDER} | grep '.avi$')
    for FILE in ${FILE_LIST}; do
        VIDEO_FILE=${1}/${FOLDER}/${FILE}
        echo "video name is ${VIDEO_FILE}"
        python demo_th.py tracking --dataset mot --load_model ../models/crowdhuman.pth --date ${FOLDER}\
                                    --demo ${VIDEO_FILE} --pre_hm --ltrb_amodal --pre_thresh 0.3\
                                    --track_thresh 0.3 --inference --clip_len 3 --trades --save_video\
                                    --resize_video --input_h 544 --input_w 960 --save_results\
                                    --exp_id thr3 --term_sec 3
    done
done
