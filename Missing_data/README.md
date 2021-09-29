# Missing Data Code

## Overview

이 폴더에는 다음과 같은 기능을 수행하는 코드들이 담겨있습니다. 

1. MongoDB를 쿼리해서 특정 기간동안 하루단위로 특정 agent가 등장하는지 확인 (`one_sensor_analysis.py`)
2. MongoDB를 쿼리해서 특정 기간동안 하루단위로 특정 context가 등장하는지 확인 (`one_sensor_analysis.py`)
3. MongoDB를 쿼리해서 특정 기간동안 하루단위로 각 종류의 agent가 등장하는지 확인 (`multi_sensor_analysis.py`)
4. MongoDB를 쿼리해서 특정 기간동안 하루단위로 각 종류의 context가 등장하는지 확인 (`multi_sensor_analysis.py`)
5. 1~4번에서 얻어낸 데이터를 heatmap으로 시각화 (`draw_plot.py`)

이외의 파일(`draw_plot2.py`, `merge_context`,  `query_agent.py`, `test.py`, `utils.py`)무시해도 좋습니다.

## Requirement

현재 제가 작업하는 환경 기준입니다.

* pandas==1.2.0
* pymongo==3.11.3
* xlrd==2.0.1
* matplotlib==3.3.4
* seaborn==0.11.1

## one_sensor_analysis.py

### 코드 설명

MongoDB를 쿼리해서 특정 기간동안 하루단위로 특정 agent 또는 context가 등장하는지 확인하는 코드입니다. 전자는 `one_sensor_analysis` 함수를 사용하고, 후자는 `one_context_analysis` 함수를 사용합니다. 

### 사용방법 (1)  one_sensor_analysis

* DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

* 코드 92번째 줄부터 확인하고 싶은 agent에 대한 내용으로 수정을 하면 됩니다. 

* 리턴 값은 각각 다음과 같습니다.

  * 시작 시간과 종료 시간 사이 하루간격의 타임스탬프 값을 가지는 numpy array (이후 그래프를 그릴때 x 축의 값으로 이용)
  * 시작 시간과 종료 시간 사이 하루 단위로 agent가 등장한 횟수의 값을 가지는 numpy array 

* 별도의 arugment 없이 코드를 동작시킨다.

  ```bash
  python one_sensor_analysis.py
  ```

```python
if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000) # 시작 타임스탬프
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000) # 종료 타임스탬프

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
    sensor_name = 'SoundSensorAgent' # 확인하고 싶은 agent 이름 (DB 상으로 publisher 명)
   	all_ts_data, all_sensor_data = one_sensor_analysis(db_info, sensor_name, start_ts, end_ts)
	
```

### 사용방법 (2)  one_context_analysis

* DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

* 코드 92번째 줄부터 확인하고 싶은 context에 대한 내용으로 수정을 하면 됩니다. 

* 리턴 값은 각각 다음과 같습니다.

  * 시작 시간과 종료 시간 사이 하루간격의 타임스탬프 값을 가지는 numpy array (이후 그래프를 그릴때 x 축의 값으로 이용)
  * 시작 시간과 종료 시간 사이 하루 단위로 context가 등장한 횟수의 값을 가지는 numpy array 

* 별도의 arugment 없이 코드를 동작시킨다.

  ```bash
  python one_sensor_analysis.py
  ```

```python
if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000) # 시작 타임스탬프
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000) # 종료 타임스탬프

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
    context_name = 'SoundWall0' # 확인하고 싶은 context 이름 (DB 상으로 name 명)
   	all_ts_data, all_sensor_data = one_context_analysis(db_info, context_name, start_ts, end_ts)
	
```

### 주의사항

* `db_info.json`파일은 Service Provision Notion에 업로드해두었습니다.
  * 경로: Service Provision->Scientific Data->Segmentation using Video
* Context 이름이나 agent 이름은 DB를 참고하거나 Service Provision Notion에 업로드한 `pair.xlsx`를 참고하면 될것 같습니다.
  * 경로: Service Provision->Scientific Data->Other Data Analysis

## multi_sensor_analysis.py

### 코드 설명

MongoDB를 쿼리해서 특정 기간동안 하루단위로 인풋으로 제공한 리스트 안의 agent 또는 context가 등장하는지 확인하는 코드입니다. 전자는 `multi_sensor_analysis` 함수를 사용하고, 후자는 `multi_context_analysis` 함수를 사용합니다. 

### 사용방법 (1)  multi_sensor_analysis

* DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

* 코드 92번째 줄부터 확인하고 싶은 agent들에 대한 내용으로 수정을 하면 됩니다. 

* 해당 함수는 리턴 값 없이 agent 리스트에 대한 하루단위의 등장 횟수의 정보가 담긴 xlsx 파일을 저장합니다.

  *  파일명: `{시작날짜}-{종료날짜}_sensor.xlsx`

* 별도의 arugment 없이 코드를 동작시킨다.

  ```bash
  python multi_sensor_analysis.py
  ```

```python
if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000) # 시작 타임스탬프
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000) # 종료 타임스탬프

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    sensor_list = load_list('agent_list.txt') # 원하는 agent list가 담긴 파일 로드
    multi_sensor_analysis(db_info, sensor_list, start_ts, end_ts)

```

### 사용방법 (2)  multi_context_analysis

* DB 정보가 담긴 json 파일 (`db_info.json`)을 본 폴더안에 넣어준다. 

* 코드 92번째 줄부터 확인하고 싶은 context들에 대한 내용으로 수정을 하면 됩니다. 

* 해당 함수는 리턴 값 없이 context 리스트에 대한 하루단위의 등장 횟수의 정보가 담긴 xlsx 파일을 저장합니다.

  *  파일명: `{시작날짜}-{종료날짜}context.xlsx`

* 별도의 arugment 없이 코드를 동작시킨다.

  ```bash
  python multi_sensor_analysis.py
  ```

```python
if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000) # 시작 타임스탬프
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000) # 종료 타임스탬프

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    context_list = load_list('context_list.txt') # 원하는 context list가 담긴 파일 로드
    multi_context_analysis(db_info, context_list, start_ts, end_ts)
```

### 주의사항

* `db_info.json`파일은 Service Provision Notion에 업로드해두었습니다.
  * 경로: Service Provision->Scientific Data->Segmentation using Video
* 각 함수의 인풋으로 들어가는 텍스트 파일의 예시는 Service Provision Notion에 업로드한 `agent_list.txt` 그리고 `context_list.txt`를 참고하면 될 것 같습니다..
  * 경로: Service Provision->Scientific Data->Other Data Analysis

## draw_plot.py

### 코드 설명

one_sensor_analysis.py와 multi_sensor_analysis.py을 통해 얻어낸 데이터를 heatmap으로 시각화하는 코드입니다. 데이터를 정규화하는 방법에 따라 총 세가지 모드로 heatmap을 생성할 수 있으며 결과는 png 파일로 저장됩니다. 3 종류의 모드는 다음과 같습니다.

1. max - 각 agent 혹은 context 데이터에 대해 해당 데이터의 max 값으로 나누는 방식으로 정규화하는 모드로, 데이터 내에서의 각 날마다의 정확한 데이터 크기비교를 하기 용이합니다.
2. mean -  각 agent 혹은 context 데이터에 대해 해당 데이터의 mean 값으로 나눈 값을 0과 1사이로 clipping 하여 정규화하는 모드로, max 모드에 비해 데이터 내에서의 각 날마다의 데이터 크기비교는 조금 부정확하지만 데이터가 적게 등장한 날의 픽셀이 더 잘보인다는 장점이 있습니다.
3. alive - 각 agent 혹은 context 데이터에 대해 1이 넘는 값들은 모두 1로 치환하여 정규화하는 모드로, 데이터 내에서의 각 날마다의 데이터 크기비교는 불가능하지만 각 날짜에 해당 데이터가 등장했는지만을 확인할 때 효과적입니다.

### 사용방법

* 코드 51번째 줄부터 확인하고 싶은 context 혹은 agent들에 대한 내용으로 수정을 하면 됩니다. 

* 해당 함수는 리턴 값 없이 결과 heatmap 이미지 파일을 저장합니다.

* 별도의 arugment 없이 코드를 동작시킨다.

  ```bash
  python draw_plot.py
  ```

```python
if __name__ == '__main__':
    file_path = '170101-180101_context.xlsx' # one_sensor_analysis.py와 multi_sensor_analysis.py을 통해 얻어낸 데이터 파일 경로
    index_name = 'context' # agent에 대한 데이터일때는 'agent'로 입력

    start_dt = datetime.datetime(2017, 1, 1, 0, 0) # heatmap 시작 일자
    end_dt = datetime.datetime(2018, 1, 1, 0, 0) # heatmap 종료 일자
    
    methods = 'max' # 원하는 모드에 따라 'max', 'mean', 'alive'로 입력
    fname = 'heatmap.png' # 결과 heatmap 파일 이름
    draw_heatmap(file_path, fname, start_dt, end_dt, method=method, index_name=index_name)
```

### 주의 사항

* 엑셀 파일의 시간 범위를 벗어나는 시작 일자와 종료 일자를 설정하면 오류가 발생할 수도 있습니다.
* 생성 되는 Heatmap 이미지의 옵션을 변경하려면 `draw_heatmap` 함수의 36번째 줄부터 48번째 줄을 수정하면 될 것입니다. 

## publisher_analysis.py

### 코드 설명

MongoDB를 쿼리해서 특정 기한 내에 등장하는 모든 context의 name과 publisher 그리고 출현 빈도를 추출하는 코드입니다. 코드의 실행 결과는 `.xlsx` 파일로 저장됩니다.
