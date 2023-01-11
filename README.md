# SD_website
데이터셋을 소개하기 위한 목적으로 만들어진 사이트입니다. 도메인은 http://doo-re.kaist.ac.kr 입니다. 이 사이트는 Flask를 기반으로 구현되었고 Nginx를 통해 배포됩니다. 아래에서 페이지의 내용을 변경하는 방법에 대해 설명합니다.

### 관리자 페이지를 통한 내용 수정

1. 관리자 페이지 접속
   - URL: http://doo-re.kaist.ac.kr/admin
   - ID: admin
   - Password: C로 시작하고 숫자가 포함되는 비밀번호
2. 내용 수정
   - 관리자 계정에 로그인 된 상태에서 home 또는 contact 페이지에 접속하면 edit 창이 띄워짐
   - Tab name, Title, Description, Content를 수정할 수 있으며 Content에는 HTML 형식으로 작성해야함
   - 수정을 완료하면 SUBMIT 버튼을 클릭함
3. 수정된 내용 확인
   - SUBMIT 버튼을 누르고 나면 수정사항이 반영된 페이지를 보여줌
   - 추가적인 수정이 필요할 경우, 우측 상단의 Edit 버튼을 클릭함


### 직접적인 코드 수정
기존 페이지에 대한 내용 변경 외에 새로운 페이지 및 기능을 추가하거나 layout을 변경하려면 코드를 직접 수정해야합니다. 작성된 코드의 위치는 아래와 같습니다.
1. VM 위치
   - 현재 DOO-RE 홈페이지가 실행되고 있는 VM에 대한 정보는 구글 스프레드 시트 `[Manual] CDSNLab Server VM / AP Allocation`에서 확인할 수 있습니다.
2. directory 경로
   - `/home/cdsn/SD_website`

수정된 코드를 반영시키려면 웹서버를 재시작해야합니다. 다음 명령어를 통해 웹서버를 재시작합니다. `systemctl restart SD_website`.



