# Segmentation Guide
## Overview
- Object detection model을 활용하여 웹캠으로 촬영된 영상 내의 사람을 감지하고, 사람이 감지된 구간을 Mongo DB에 저장합니다.
- Mongo DB에 저장되는 항목은 해당 segment의 시작 시간, 종료 시간, 감지된 사람의 평균 수 입니다.

## Object detection model
- CVPR 2021에 출판된 논문인 "Track to Detect and Segment: An Online Multi-Object Tracker"에서 제안된 human tracking 모델 TraDeS를 segmentation에 사용합니다.
- 따라서 [TraDes github](https://github.com/JialianW/TraDeS)에 접속하여 해당 repository를 clone하는 과정이 필요합니다.


## 파일 설명
- 이 디렉토리 내에 존재하는 `demo_th.py`와 `demo.sh`를 
### demo_th.py