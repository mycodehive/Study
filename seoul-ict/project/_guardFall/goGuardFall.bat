@echo off
goto menu

:: ========== 단계 함수들 ==========

:step1
echo [1] Python 설치 파일 다운로드 중...
curl -o python-3.10.0-amd64.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
echo [완료] 설치 파일 다운로드됨.
pause
goto menu

:step2
echo [2] Python 설치 중...
start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 TargetDir=C:\Python310 Include_launcher=0 Include_test=0 PrependPath=0
if not exist C:\Python310\python.exe (
    echo [오류] Python 설치 실패!
) else (
    echo [완료] Python 설치됨: C:\Python310
)
pause
goto menu

:step3
echo [3] pip 설치 및 업그레이드 중...
C:\Python310\python.exe -m ensurepip
C:\Python310\python.exe -m pip install --upgrade pip
echo [완료] pip 설치됨.
pause
goto menu

:step4
echo [4] 가상환경 생성 중...
cd /d %~dp0
C:\Python310\python.exe -m venv guardfall_env
echo [완료] 가상환경 생성됨.
pause
goto menu

:step5
echo [5] 가상환경 활성화 및 pip upgrade 설치 중...
call guardfall_env\Scripts\activate
pip install --upgrade pip
echo [완료] 활성화 완료.
pause
goto menu

:step6
echo [6] 가상환경 비활성화
call guardfall_env\Scripts\activate
deactivate
pause
goto menu

:: ========== 메뉴 ==========

:menu
cls
echo =====================================================
echo  GuardFall 환경설정 마법사(관리자모드로 실행하세요)
echo =====================================================
echo [1] Python(3.10) 설치 파일 다운로드
echo [2] Python(3.10) 설치
echo [3] pip 설치 및 업그레이드
echo [4] 가상환경 생성
echo [5] 가상환경 활성화
echo [6] 가상환경 비활성화
echo [0] 종료
echo ----------------------------------------
set /p choice="실행할 단계 번호를 입력하세요 (0~6): "

if "%choice%"=="1" goto step1
if "%choice%"=="2" goto step2
if "%choice%"=="3" goto step3
if "%choice%"=="4" goto step4
if "%choice%"=="5" goto step5
if "%choice%"=="6" goto step6
if "%choice%"=="0" exit

echo [!] 잘못된 입력입니다. 다시 선택하세요.
pause
goto menu
