uv 사용 예시

(1) 프로젝트 초기화
uv init
또는 특정 폴더로 초기화:
uv init my_project

(2) 패키지 설치
uv add streamlit

(3) 패키지 제거
uv remove streamlit

(4) 실행
uv run main.py

(5) Python 버전 바꾸기
echo 3.11.7 > .python-version
Python 버전 변경 시 pyproject.toml 파일도 업데이트하는 것이 좋습니다:

[project]
requires-python = ">=3.11.7"
uv run main.py 실행 시 필요한 Python 버전이 자동으로 설치되므로, 별도 설치 과정 없이도 프로젝트 실행이 가능합니다.