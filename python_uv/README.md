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

---

## 📦 설치

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

또는 `Homebrew` (macOS, Linux):

```bash
brew install astral-sh/uv/uv
```

---

## 🚀 기본 사용법

### 1. 프로젝트 초기화

```bash
uv init
```

- `pyproject.toml` 생성됨
- PEP 621 형식으로 프로젝트 설정 가능

---

### 2. 패키지 설치

```bash
uv pip install requests
```

- `pip install` 대체
- `uv.lock`에 lock 기록 가능

---

### 3. 종속성 정리 및 고정 (`lock` 파일 생성)

```bash
uv pip compile
```

- `requirements.txt`나 `uv.lock` 생성
- `pip-tools`의 `pip-compile` 역할 수행

---

### 4. 종속성 설치

```bash
uv pip sync
```

- `uv.lock` 또는 `requirements.txt` 기반으로 정확하게 패키지 설치

---

### 5. 런타임 실행

```bash
uv venv exec python app.py
```

- 가상환경 생성 및 실행도 가능 (원하면 `.venv` 또는 PEP 582 방식 선택 가능)

---

## 📁 구조 예시

```plaintext
project/
├── pyproject.toml
├── uv.lock
├── __pypackages__/         ← 가상환경 없이 로컬 설치될 경우 위치
└── app.py
```

---

## 🔄 `uv` vs `pip` vs `poetry` vs `pip-tools`

| 도구        | 언어 | 속도   | 가상환경 | Lock 지원 | 사용성 |
|-------------|------|--------|-----------|------------|--------|
| `uv`        | Rust | 🔥 매우 빠름 | 선택적 (`__pypackages__`) | ✅ `uv.lock` | modern + CLI 통합 |
| `pip`       | Python | 보통 | 필요 (`venv`) | ❌ | 단순 |
| `poetry`    | Python | 느림 | 자동 관리 (`.venv`) | ✅ | 직관적이나 느림 |
| `pip-tools` | Python | 보통 | 필요 | ✅ | `requirements.txt` 기반 |

---

## 📌 언제 `uv`를 쓰면 좋을까?

- `pip`보다 더 빠르고 정확한 설치가 필요할 때
- Docker에서 가상환경 없이 빠르게 패키지를 설치하고 싶을 때
- `poetry`처럼 lockfile 기반 프로젝트 관리를 하고 싶지만, 더 빠른 도구가 필요할 때
- `pyproject.toml` 기반의 현대적인 Python 프로젝트 구성을 원할 때
