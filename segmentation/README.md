# Segmentation Guide
## Overview
- Object detection model을 활용하여 웹캠으로 촬영된 영상 내의 사람을 감지하고, 사람이 감지된 구간을 Mongo DB에 저장합니다.
- Mongo DB에 저장되는 항목은 해당 segment의 시작 시간, 종료 시간, 감지된 사람의 평균 수 입니다.

### Object detection model
- CVPR 2021에 출판된 논문인 "Track to Detect and Segment: An Online Multi-Object Tracker"에서 제안된 human tracking 모델 TraDeS를 segmentation에 사용합니다.
- 따라서 [TraDes github](https://github.com/JialianW/TraDeS)에 접속하여 해당 repository를 clone하는 과정이 필요합니다.


## 파일 설명
- 이 디렉토리 내에 존재하는 `demo_th.py`와 `demo.sh`를 `./TraDeS/src/` 로 옮깁니다.
### demo_th.py
- human tracking 후 얻어지는 `*.avi_result.json` 파일을 활용해서 activity episode의 시작 지점, 종료 지점 및 평균 사람 수를 json format으로 저장
- activity episode
    - n초 내에 존재하는 프레임들은 하나의 그룹액티비티 에피소드로 합침
    - term_sec 인수를 통해 n을 지정할 수 있음
- *.avi_episode.json 예시
    - `{"0": {"start": "00:20:03", "end": "00:20:07", "avg_n_human": 1.0}, "1":{...}, ...}`
    - avg_n_human: 해당 에피소드에서 감지된 사람 수의 평균
- 실행 명령어
    ```
    python demo_th.py tracking --dataset mot --load_model ../models/crowdhuman.pth --date 20210413 --demo ../nas/20210413/HSL-492641-GLULE/20210413_151628.avi --pre_hm --ltrb_amodal --pre_thresh 0.3 --track_thresh 0.3* --inference --clip_len 3 --trades --resize_video --input_h 544 --input_w 960 --exp_id test --term_sec 3 --save_video --save_results
    ```