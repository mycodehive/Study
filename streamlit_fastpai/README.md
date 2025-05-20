<pre>
PS C:\streamlit_fastpai\backend> uv init
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

[각각]
.venv\Scripts\activate
uv add -r requirements.txt

[terminal 1] - 항상 이것부터 먼저 실행
  - backend>uvicorn main:app --reload --host 0.0.0.0 --port 8000

[terminal 2]
  - frontend>uv run -- streamlit run app.py
