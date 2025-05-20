### Step 1
  - uv package 라이브러리 설치
    - window : <pre>powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"</pre>
    - mac : <pre>curl -LsSf https://astral.sh/uv/install.sh | sh</pre>
  - 확인 : uv --version
    
<pre>
PS C:\streamlit_fastpai\backend> uv init -p 3.12
Initialized project `backend`
PS C:\streamlit_fastpai\backend> uv venv --python 3.12
Using CPython 3.12.9
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
PS C:\streamlit_fastpai\backend> cd ..
PS C:\streamlit_fastpai> cd .\frontend\
PS C:\streamlit_fastpai\frontend> uv init
Initialized project `frontend`
PS C:\streamlit_fastpai\frontend> uv venv --python 3.12
Using CPython 3.12.9
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
</pre>

### Step 2
[각각]
  - .venv\Scripts\activate
  - uv add -r requirements.txt

### Step 3
[terminal 1] - 항상 이것부터 먼저 실행
  - backend>uv run -- uvicorn main:app --reload --host 0.0.0.0 --port 8000

[terminal 2]
  - frontend>uv run -- streamlit run app.py

---
### Step 4
[DB]
  - https://dbeaver.io/download/
