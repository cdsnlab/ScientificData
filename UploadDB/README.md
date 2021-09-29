# Upload DB Code

## Overview

이 폴더에는 다음과 같은 기능을 수행하는 코드들이 담겨있습니다. 

1. Annotation한 Activity 데이터를 MongoDB로 업로드 (`upload_annotation.py`)
2. MongoDB에 있는 Sensor 데이터와 Activity 데이터를 활용하여 각 Activity가 진행되는 동안의 센서데이터를 수집하여 하나의 CSV 파일에 저장 (`query_sensor_activity.py`, `query_data.py `)
3. 기존의 메타데이터에 `sensor_name`행을 추가 (`add_sensor_name.py`)

이외의 파일(`correct_time.py`, `filename_extract.py`, `test.py`)에 대해서는 무시해도 좋습니다.

## Requirement

현재 제가 작업하는 환경 기준입니다.

* pandas==1.2.0
* pymongo==3.11.3
* xlrd==2.0.1

## upload_annotation.py

### 코드 설명

Goolge Speard Sheet에서 Annotation한 Activity 데이터를 MongoDB로 업로드하는 코드입니다. 업로드는 N1SeminarRoom825_Annotation Collection에 저장되며 DB의 업로드 되는 정보는 다음과 같습니다.

1. 날짜 (String)
2. 관련 비디오 파일명 (String)
3. 시작시간 (Int, Timestamp)
4. 종료시간 (Int, Timestamp)
5. 레이블 (String)
6. 기간 (Int, 단위: msec)
7. 평균 사람 수 (Float)

### 사용 방법

1. 스프레드 시트 파일을 엑셀로 저장하여 본 폴더안에 넣어준다. (파일->다운로드->Microsoft Excel(.xlsx))

   * 파일명은 기본값인 `SeminarRoom_Labeling.xlsx`로 해주세요.

2. DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

3. 별도의 argument 없이 코드를 동작 시킨다.

   ```bash
   python upload_annotation.py
   ```

### 주의 사항

* 기존에 작성한 코드에서 레이블 데이터를 엑셀 파일의 '레이블' 열에서 추출하도록 설계가 되어있습니다. Cross check가 끝난 이후에는 레이블 데이터를 최종 레이블 데이터가 적힌 열에서 추출하도록 코드를 변경해주세요.
  *  `upload_annotation.py` 의 29번째 줄의 '레이블'이라고 적힌 부분을 최종 레이블 데이터가 적힌 열의 header의 이름으로 대체하면 될것입니다.

* `db_info.json`파일은 Service Provision Notion에 업로드해두었습니다.
  * 경로: Service Provision->Scientific Data->Segmentation using Video

## query_sensor_activity.py 

### 코드 설명

MongoDB에 있는 Sensor 데이터와 Activity 데이터를 활용하여 각 Activity가 진행되는 동안의 센서데이터를 수집하여 하나의 CSV 파일에 저장하는 코드입니다. N1SeminarRoom825_Annotation collection을 우선적으로 쿼리하여 9월 부터 12월동안의 모든 Activity 데이터를 추출한 후, 각 activity의 시작과 끝나는 지점의 타임스탬프 사이의 센서데이터를 수집하는 형식으로 설계되었습니다. 본 코드를 통해 저장되는 데이터는 다음과 같습니다.

1. 센서 데이터
   * `sensor` 폴더에 저장되며, {레이블}_{시작 지점의 타임스탬프}.csv의 형태로 저장
   * 각 context의 timestamp, publisher, context name, value 값들이 저장
   * action에 해당하는 context의 경우 value값이 없습니다 (빈칸으로 처리).
2. 메타 데이터
   * `metadata` 폴더에 저장되며, {레이블}_{시작 지점의 타임스탬프}.txt의 형태로 저장
   * 해당 activity의 label, start timestamp, end timestamp, average number of human 값들이 저장

### 사용 방법

1. DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

2. 별도의 argument 없이 코드를 동작 시킨다.

   ```bash
   python query_sensor_activity.py
   ```

### 주의 사항

* `upload_annotation.py`을 통해 activity 데이터가 N1SeminarRoom825_Annotation collection에 저장된 이후에 본 코드를 사용해야 합니다. 
* `db_info.json`파일은 Service Provision Notion에 업로드해두었습니다.
  * 경로: Service Provision->Scientific Data->Segmentation using Video

## query_data.py 

### 코드 설명

MongoDB에 있는 Sensor 데이터와 Activity 데이터를 활용하여 각 Activity가 진행되는 동안의 센서데이터를 수집하여 하나의 CSV 파일에 저장하는 코드입니다. `query_sensor_activity.py`와 다르게 각 context마다 새로운 sensor name을 부여하였다. N1SeminarRoom825_Annotation collection을 우선적으로 쿼리하여 9월 부터 12월동안의 모든 Activity 데이터를 추출한 후, 각 activity의 시작과 끝나는 지점의 타임스탬프 사이의 센서데이터를 수집하는 형식으로 설계되었습니다. 본 코드를 통해 저장되는 데이터는 다음과 같습니다.

1. 센서 데이터
   * `sensor` 폴더에 저장되며, {레이블}_{시작 지점의 타임스탬프}.csv의 형태로 저장
   * 각 context의 timestamp, sensor_name, value 값들이 저장
2. 메타 데이터
   * `metadata` 폴더에 저장되며, {레이블}_{시작 지점의 타임스탬프}.txt의 형태로 저장
   * 해당 activity의 label, start timestamp, end timestamp, average number of human, duration 값들이 저장

### 사용 방법

1. DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

2. 별도의 argument 없이 코드를 동작 시킨다.

   ```bash
   python query_data.py
   ```

### 주의 사항

* `upload_annotation.py`을 통해 activity 데이터가 N1SeminarRoom825_Annotation collection에 저장된 이후에 본 코드를 사용해야 합니다. 
* `db_info.json`파일은 Service Provision Notion에 업로드해두었습니다.
  * 경로: Service Provision->Scientific Data->Segmentation using Video

## add_sensor_name.py

### 코드 설명

`metadata` 폴더 안에 있는 메타데이터 파일에 해당 에피소드 동안 등장한 모든 sensor name을 리스트화하여 기록하는 코드입니다. 예를들어 메타데이터 파일 `Eating together_1504767471000.txt`에 센서데이터 `Eating together_1504767471000.csv`의 `sensor_name` 리스트를 기록합니다.