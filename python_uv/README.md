## 🐍 Python 패키지 관리 도구 `uv`란?

> `uv`는 Astral(예전의 Astral.sh, 현재는 `pdm`, `rye` 등에 기여 중)에서 만든 **초고속 Python 패키지 관리 툴**입니다. Rust로 작성되어 기존의 `pip`, `poetry`, `virtualenv`보다 빠르면서도 다양한 기능을 하나로 통합한 것이 특징입니다.

---

## ✅ 주요 특징

| 기능 | 설명 |
|------|------|
| 🏃‍♂️ 빠른 설치 속도 | Rust로 작성되어 `pip`, `poetry`보다 훨씬 빠름 |
| 🔧 PEP 582 지원 | `__pypackages__` 기반 로컬 패키지 설치 (가상환경 불필요) |
| 🧰 종속성 해결 | `pip-tools` 스타일의 정확한 dependency resolution |
| 🗂️ `pyproject.toml` 지원 | Poetry 스타일 프로젝트 설정 가능 |
| 🧪 가상환경 없이 동작 가능 | `.venv` 없이도 작동하는 lightweight한 프로젝트 관리 |
| 🔁 Lockfile 지원 | reproducible install 지원 (`uv.lock`) |
| 🐳 Docker 친화적 | 속도와 구조상 컨테이너에서 유리 |

## pip vs uv

|구분|만들 때|협업 할 때|
|:------:|------|------|
|pip|python -m venv venv<br>venv\scripts\activate<br>pip install openai<br>python main.py<br>pip freeze > requirements.txt|python -m venv venv<br>venv\scripts\activate<br>pip install -r requirements.txt<br>python main.py|
|uv|uv init<br>uv add openai<br>uv run main.py|uv run main.py|

## 참고 사이트
  - https://docs.astral.sh/uv/
  - https://github.com/dabidstudio/uv_python_example
  - https://github.com/dabidstudio/dabidstudio_guides/blob/main/python_uv.md
  - https://github.com/dabidstudio/youtubeinsights-mcp-server
  - https://www.youtube.com/watch?v=1kZ-touiEQ8
